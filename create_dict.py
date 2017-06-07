import string
import math
import re
from collections import Counter
from functools import reduce



abusive=open('abusivewords.txt','r')
abusive_list=abusive.read().split("\n")

# convert all the data from the sample corpus to lower case letters and remove all extra space
# and replace it by a single space.Remove the new line characters

bi_probability_dict={}
tri_probability_dict={}
four_probability_dict={}
bigram_list = []
fourgram_list = []
unigram_list = []
trigram_list = []

def get_bigrams(unigram):
    for i in range(len(unigram)-1):
        bigram_list.append(unigram[i]+':'+unigram[i+1])
        if unigram[i] in bi_probability_dict and unigram[i+1] not in \
                bi_probability_dict[(unigram[i])]:
            bi_probability_dict.get(unigram[i]).append(unigram[i + 1])
            continue

        bi_probability_dict[unigram[i]] = [unigram[i + 1]]

    return (bigram_list)


def write_into_files(file_type,file_dict):
    file1 = open('filedata/' + file_type + '.txt', 'w')
    for key,val in file_dict.items():
        file1.write(str(key) +'$' + str(val) + '\n')
        #print(str(key) +' ' + str(val) + '\n')
    print('done')


def get_trigrams(unigram):
    for i in range(len(unigram)-2):
        trigram_list.append(unigram[i]+":"+unigram[i+1]+":"+unigram[i+2])
        if (unigram[i]+":"+unigram[i+1]) in tri_probability_dict and unigram[i+2] not in \
                tri_probability_dict[unigram[i]+":"+unigram[i+1]] :
            tri_probability_dict.get(unigram[i]+":"+unigram[i+1]).append(unigram[i + 2])
            continue

        tri_probability_dict[unigram[i]+":"+unigram[i+1]] = [unigram[i + 2]]


    return (trigram_list)

def get_4_grams(unigram):

    for i in range(len(unigram)-3):
        fourgram_list.append(unigram[i]+":"+unigram[i+1]+":"+unigram[i+2]+":"+unigram[i+3])
        if ((unigram[i]+":"+unigram[i + 1]+":"+unigram[i + 2])) in four_probability_dict and unigram[i+3] not in \
                four_probability_dict[unigram[i]+":"+unigram[i+1]+":"+unigram[i+2]]:
            four_probability_dict.get(unigram[i]+":"+unigram[i + 1]+":"+unigram[i+2]).append(unigram[i + 3])
            continue
        four_probability_dict[unigram[i]+":"+unigram[i + 1]+":"+unigram[i+2]] = [unigram[i + 3]]
    return (fourgram_list)

"""
This function generates the n-gram tables
"""

def populate_ngrams(unigram_list):
    bigram_list = get_bigrams(unigram_list)
    trigram_list=get_trigrams(unigram_list)
    fourgram_list=get_4_grams(unigram_list)

    unigram_dict = dict(Counter(unigram_list))
    bigram_dict = dict(Counter(bigram_list))
    trigram_dict = dict(Counter(trigram_list))
    fourgram_dict = dict(Counter(fourgram_list))

    write_into_files('unigram', unigram_dict)
    write_into_files('bigram', bigram_dict)
    write_into_files('trigram', trigram_dict)
    write_into_files('fourgram', fourgram_dict)
    write_into_files('bi_dict', bi_probability_dict)
    write_into_files('tri_dict', tri_probability_dict)
    write_into_files('four_dict', four_probability_dict)



# Read the data corpus and convert all the text to lower case.Remove all punctuations and unicode characters.
# split the data based on space present
# For now the below code evaluates 10% of the data.In order to check for a different amount of data set change the
# if statement to line_count < 10102 for 1%, 30307 for 3%,50512 for 5% and 1010242 for 100% of the entire data set.


with open('news.txt',encoding='utf8') as f:
    line_count=0
    unigram_list = []
    for line in f:
        if line_count<101024:
            line_count=line_count+1
            line=''.join(filter(lambda x: x in string.printable, line))
            line = line.lower()
            line = line.replace('\n', '').replace("“", '"').replace("”", '"').replace("’", "'")
            trans = str.maketrans('', '', string.punctuation)
            line = line.translate(trans)
            line = line.replace('\n', '').replace("“", '"').replace("”", '"').replace("’","'")
            line = re.sub('\s+', ' ', line).strip()
            line=line.split(" ")
            unigram_list.extend(line)





#Once we get the data , we remove any abusive language present in the code.
unigram_list=[x for x in unigram_list if x not in abusive_list]

#Use the below code to populate the data
populate_ngrams(unigram_list)
