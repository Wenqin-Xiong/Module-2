import os
os.chdir("C:\\Users\\Ibara Jin\\Desktop\\伊原尋\\(学习)解読不能\\STAT628统计实习\\Module2") 

import pandas as pandas
import nltk
import time
import re
import numpy as np

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

data = pandas.read_csv('train_data.csv')

nreviews=data.shape[0]

data_txt=data["text"]
data_txt=data_txt[0:nreviews]

from nltk.corpus import stopwords

stop = set(stopwords.words("english"))
stop_neg=["wasn't",'wasn',"couldn't",'couldn',
          "wouldn't",'wouldn',"shouldn't",'shouldn',"shan't",
          "haven't","hasn't","hadn't","hadn'",
          "don't",'don',"doesn't",'doesn',"didn't",
          "needn't",'needn','no','nor',
          "isn't",'isn',"aren't","weren't",'weren',"won't",
          "cannot","never","dont"]
stop_revised=[w for w in stop if not w in stop_neg]
stop.add("cannot")
stop.add("never")
stop.add("dont")
stop_neg=set(stop_neg)
stop_revised=set(stop_revised)

def stop_delete(sentence):
    sentence=sentence.lower().split(" ")
    sen=[word for word in sentence if not word in stop]
    sen_re=np.array([])
    for j in sen:
        word_re=re.sub('[^a-zA-Z]','', j)
        if word_re != "":
            sen_re=np.append(sen_re,word_re)
    return sen_re

def stop_delete_re(sentence):
    sentence=sentence.lower().split(" ")
    sen=[word for word in sentence if not word in stop_revised]
    sen_re=np.array([])
    for j in sen:
        if j in stop_neg:
            sen_re=np.append(sen_re,"neg_w")
        else:
            word_re=re.sub('[^a-zA-Z]','', j)
            if word_re != "":
                sen_re=np.append(sen_re,word_re)
    return sen_re

from collections import defaultdict
from nltk.stem.wordnet import WordNetLemmatizer 
from nltk.stem.porter import PorterStemmer 

lem = WordNetLemmatizer()
stem = PorterStemmer()

#clear text
document=[]
document_re=[]
for sen in data_txt:
    txt=stop_delete(sen)
    txt_re=stop_delete_re(sen)
    
    txt=[stem.stem(word) for word in txt]
    txt_re=[stem.stem(word) for word in txt_re]
    
    document.append(txt)
    document_re.append(txt_re)
    
#frequency, threshold=min_freq
min_freq=100 
    
frequency=defaultdict(int)
#intensity
freq_pos=defaultdict(int)
freq_neg=defaultdict(int)

score=data["stars"]

for i in range(nreviews):
    sen=document[i]
    for word in sen:
        frequency[word] += 1
        if score[i] > 3:
            freq_pos[word] += 1
        elif score[i] < 3:
            freq_neg[word] += 1
            
#document=[[word for word in sen if frequency[word] > min_freq] for sen in document]
#document_re=[[word for word in sen if frequency[word] > min_freq] for sen in document_re]

frequency_dict={}
key=set(list(frequency))
for word in key:
    if word not in freq_pos:
        freq_pos[word]=0
    if word not in freq_neg:
        freq_neg[word]=0    
    if frequency[word] <= min_freq:
        del frequency[word]
        del freq_pos[word]
        del freq_neg[word]
    else:
        frequency_dict[word]=[frequency[word],freq_pos[word],freq_neg[word]]
        
document=[[word for word in sen if word in frequency] for sen in document]

freq_re=set(list(frequency))
freq_re.add("neg_w")

document_re=[[word for word in sen if word in freq_re] for sen in document_re]

data_w=data[0:nreviews]
data_w=data_w.drop("text", axis=1)

text=[]

for i in range(nreviews):
    sen=document_re[i]
    txt=""
    for w in sen:
        txt=txt+w+" "
    text.append(txt)

data_w["text"]=text    
        
data_w.to_csv("data_cleaned.csv", sep=',')

import csv

with open('document.csv', 'w', newline="") as myfile:
    writer = csv.writer(myfile)
    writer.writerows(document)
    
with open('document_re.csv', 'w', newline="") as myfile:
    writer = csv.writer(myfile)
    writer.writerows(document_re)

with open('frequency.csv', 'w', newline="") as myfile:
    writer = csv.writer(myfile)
    writer.writerow(["word","count","pos","neg"])
    for key, value in frequency_dict.items():
        writer.writerow([key, value[0],value[1],value[2]])