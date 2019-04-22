#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 11:04:58 2018

@author: mromiario
"""

#M ROMI ARIO
#1301154311

import xlrd
import nltk
import operator
import re

""" PEMBANGUNAN MODEL BIGRAM DARI KUMPULAN ARTIKEL
"""

dataset = xlrd.open_workbook('DATA_1301154311.xlsx') #membaca file dataset dari excel
data = dataset.sheet_by_index(0)
len_data = data.nrows

dataset = [] #array untuk menampung dataset
for i in range(len_data) :
    dataset.append(str(data.cell_value(i,1))) #menyimpan dataset ke array
    dataset[i] = dataset[i].lower() #membuat menjadi huruf kecil
    dataset[i] = re.sub('[^a-z]', ' ', str(dataset[i])) #menyeleksi teks yang disimpan hanya karakter a-z
    dataset[i] = nltk.word_tokenize(dataset[i]) #tokenisasi
    
freq_tab = {} #dict. untuk unigram
total_count = 0 #initial counter
for i in range(len_data) :
    for j in range(len(dataset[i])) :
        if dataset[i][j] in freq_tab:
            freq_tab[dataset[i][j]] += 1 #menambah jumlah counter apabila data sudah ada di dict
        else:
            freq_tab[dataset[i][j]] = 1 #apabila data baru ditambahkan ke dict
    total_count += 1        


bigram_tab = {} #dict. untuk trigram

#Perulangan untuk membuat tabel n x n yang nantinya berisi dict. frekuensi bigram 
for i in range(len_data) :
    for j in range(len(dataset[i])) :
        if dataset[i][j] not in bigram_tab:
           bigram_tab[dataset[i][j]] = {} #membuat dict. baru (dict dalam dict)
           for k in range(len_data) :
               for l in range(len(dataset[k])) :
                   if dataset[k][l] not in bigram_tab[dataset[i][j]]:
                       bigram_tab[dataset[i][j]][dataset[k][l]] = 1 #inisialisi awal setiap kata di dict.
                
#Perulangan untuk menghitung frekeunsi w+1 (kata selanjutnya) dari setiap kata
for i in range(len_data):
    for j in range(len(dataset[i])) :
        if j+1<len(dataset[i]) : #apabila kata tersebut bukan kata terakhir di artikel tsb.
            next_word = dataset[i][j+1]
            bigram_tab[dataset[i][j]][next_word] +=1 #Menambah counter apabila kata tersebut merupakan kata setelahnya

#Perulangan untuk normalisasi dengan pembagian dengan frekuensi unigram
for key_bigram in bigram_tab.keys() :
    for key_uni in freq_tab.keys() :
        value = bigram_tab[key_bigram][key_uni] 
        bigram_tab[key_bigram][key_uni] = value/freq_tab[key_bigram] #Melakukan perhitungan probabilitas
   
"""Pengujian Prediksi Kemunculan Kata
"""

predicted_word = ['dilansir','jakarta','pagi','ibu','berita','pemandangan','menyumbang','anti','memakan','di','bandung']
#1. dilansir : kata beriumbuhan di
#2.jakarta : nama kota
#3. pagi : keterangan waktu
#4. ibu : kata ganti
#5.berita : kata benda
#6. pemandangan : kata berimbuhan pe-an
#7. menyumbang : kata berimbuhan me-
#8. anti = kata negasi
#9. memakan = kata berimbuhan me-an
#10. di = kata depan
#bandung = kata tidak ada di dictionary

for i in range(len(predicted_word)) :
    if predicted_word[i] not in bigram_tab :
        print("kata:",predicted_word[i],"tidak terdapat di dictionary")
    else :
        print("prediksi kata selanjutnya:",predicted_word[i],"-", max(bigram_tab[predicted_word[i]].items(), key=operator.itemgetter(1))[0]) 
        #Mengeluarkan kata dengan nilai probabilitas paling tinggi
        
""" Evaluasi dengan Perplexity
"""

sentence =  ["negara empat musim hingga kini masih mengalami musim dingin", 
             "Tidak bisa dibayangkan dengan apapun bagaimana dinginnya kota tersebut.",
              "Indonesia, khususnya Jakarta akhir-akhir ini sering diguyur hujan",
              "setiap orang yang memiliki makanan dan minuman kesukaan masing-masing."
              ,"Semua orang yang olahraga pasti punya tujuan ingin membakar kalori."]


for i in range(len(sentence)) :
    sentence[i] = sentence[i].lower() #membuat menjadi huruf kecil
    sentence[i] = re.sub('[^a-z]', ' ', str(sentence[i])) #menyeleksi teks yang disimpan hanya karakter a-z
    sentence[i] = nltk.word_tokenize(sentence[i]) #tokenisasi

temp = 1 #inisialisasi awal menyimpan hasil perkalian likelihood probability
N = 0 #menghitung jumlah bigram pada dataset
for i in range (len(sentence)) :
    for j in range(len(sentence[i])) :
        N +=1
        if j+1<len(sentence[i]) : #apabila kata tersebut bukan kata terakhir di artikel tsb.
            next_word = sentence[i][j+1]
            if ((sentence[i][j] in freq_tab) and next_word in freq_tab) :
                temp = temp*bigram_tab[sentence[i][j]][next_word] #melakukan perkalian probabilitas
            else :
                temp = temp*0.0001 #memberi nilai yang sangat kecil apabila probabilitas pada data tester tidak ditemukan
        else :
            temp = temp*0.0001 #memberi nilai yang sangat kecil apabila probabilitas pada data tester tidak ditemukan
            
preplexity = (1/temp)**(1/N) #melakukan 1/probability dan diakarkan dengan akar N
print(preplexity)
