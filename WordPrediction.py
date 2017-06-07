import string
import math
import re
from collections import Counter
import os
import ast
import operator


smoothing=0.1
V=37


def ngram_data(path_c,filename):
    data=open(path_c+filename,'r')
    data=data.read().strip().split("\n")

    new_dict = {}
    for i in data:
        new_data = i.split("$")
        new_dict.update({new_data[0]: new_data[1]})

    return new_dict
list_of_words = {}

def get_prob(n1,n2):
    prob = float(n1 + smoothing)/(n2 + V*smoothing)
    return prob

def check_fourgram(n1,four,tri,four_ngram):
    if n1 in four_ngram:
        #print(four_ngram[n1])
        words= four_ngram[n1]
        words=ast.literal_eval(words)
        #print(words)
        for i in words:
            count_n1=int(four[n1+':'+i])
            count_n2=int(tri[n1])
            prob=get_prob(count_n1,count_n2)
            list_of_words.update({i:prob})
    return list_of_words

def check_trigram(n1,tri,bi,tri_ngram):
    if n1 in tri_ngram:
        #print(four_ngram[n1])
        words= tri_ngram[n1]
        words=ast.literal_eval(words)
        #print(words)
        for i in words:
            count_n1=int(tri[n1+':'+i])
            count_n2=int(bi[n1])
            prob=get_prob(count_n1,count_n2)
            list_of_words.update({i:prob})

    return list_of_words

def check_bigram(n1,bi,uni,bi_ngram):
    if n1 in bi_ngram:
        words= bi_ngram[n1]
        words=ast.literal_eval(words)
        #print(words)
        #print(words)
        for i in words:
            count_n1=int(bi[n1+':'+i])
            count_n2=int(uni[n1])
            prob=get_prob(count_n1,count_n2)
            list_of_words.update({i:prob})

    return list_of_words


def predict_word(input_data,uni,bi,tri,four,bi_ngram,tri_ngram,four_ngram):

    if len(input_data)>=3:
        text=input_data[len(input_data)-3:len(input_data)]
        #print(text,text[1:])
        check_fourgram(':'.join(text),four,tri,four_ngram)

    if len(input_data)>=2:
        text=input_data[len(input_data)-2:len(input_data)]
        #print(text,text[1:])
        check_trigram(':'.join(text),tri,bi,tri_ngram)

    if len(input_data)>=1:
        text=input_data[len(input_data)-1:len(input_data)]
        #print(text)
        check_bigram(text[0],bi,uni,bi_ngram)

    else:
        print("Enter one or more words")

    possible_words = [v[0] for v in sorted(list_of_words.items(), key=lambda kv: (-kv[1]))]
    list_of_words.clear()
    #print(possible_words)
    return possible_words



def eval(uni,bi,tri,four,bi_ngram,tri_ngram,four_ngram):
    success=0
    failure=0
    line = open("testing_data.txt",encoding='utf8').read()
    line = ''.join(filter(lambda x: x in string.printable, line))
    line = line.lower()
    line = line.replace('\n', '').replace("“", '"').replace("”", '"').replace("’", "'")
    trans = str.maketrans('', '', string.punctuation)
    line = line.translate(trans)
    line = line.replace('\n', '').replace("“", '"').replace("”", '"').replace("’", "'")
    line = re.sub('\s+', ' ', line).strip()
    line = line.split(" ")
    #print(line)

    for i in range(0,len(line)-1):

        words=predict_word(line[:i+1],uni,bi,tri,four,bi_ngram,tri_ngram,four_ngram)
        if line[i+1] in words:
            success=success+1
        else:
            failure=failure+1

    print("Words in data corpus:", len(uni),"\tAccuracy:",(success/len(line))* 100 ,"%")



def eval_data(file):
    uni = ngram_data(file, 'unigram.txt')
    bi = ngram_data(file, 'bigram.txt')
    tri = ngram_data(file, 'trigram.txt')
    four = ngram_data(file, 'fourgram.txt')
    bi_ngram = ngram_data(file, 'bi_dict.txt')
    tri_ngram = ngram_data(file, 'tri_dict.txt')
    four_ngram = ngram_data(file, 'four_dict.txt')

    eval(uni,bi,tri,four,bi_ngram,tri_ngram,four_ngram)



def get_accuracy_on_data():
    eval_data('filedata/')
    #eval_data('filedata_1/')
    #eval_data('filedata_3/')
    #eval_data('filedata_5/')
    #eval_data('filedata_10/')


def try_it_urself():
    i=0
    file='filedata/'
    uni = ngram_data(file, 'unigram.txt')
    bi = ngram_data(file, 'bigram.txt')
    tri = ngram_data(file, 'trigram.txt')
    four = ngram_data(file, 'fourgram.txt')
    bi_ngram = ngram_data(file, 'bi_dict.txt')
    tri_ngram = ngram_data(file, 'tri_dict.txt')
    four_ngram = ngram_data(file, 'four_dict.txt')

    while i < 10:
        input_data = input("Enter the data to predict the next word\n").lower().split()
        print("Predicted Words:\n",predict_word(input_data, uni, bi, tri, four, bi_ngram, tri_ngram, four_ngram))
        i=i+1


#Run this function to check for accuracy
get_accuracy_on_data()

#The below function will let you enter your own data and predict the next word.Make sure the create_dict.py file is
# executed first
try_it_urself()