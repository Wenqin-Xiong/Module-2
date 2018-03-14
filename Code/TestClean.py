# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 16:28:29 2018

@author: Ibara Jin


"""
data_test = pandas.read_csv('testval_data.csv')

nreviews_test=data_test.shape[0]

data_txt_test=data_test["text"]
data_txt_test=data_txt_test[0:nreviews_test]

lem = WordNetLemmatizer()
stem = PorterStemmer()

#clear text
document_re_test=[]
for sen in data_txt_test:
    txt_re=stop_delete_re(sen)    
    txt_re=[stem.stem(word) for word in txt_re]    
    document_re_test.append(txt_re)
    
document_re_test=[[word for word in sen if word in freq_re] for sen in document_re_test]

r_del=[]
for i in range(nreviews_test):
    sen=document_re_test[i]
    if sen==[]:
        r_del.append(i)

document_re_test=[sen for sen in document_re_test if sen!=[]]

data_w_test=data_test.drop(r_del)
data_w_test=data_w_test.drop("text", axis=1)

text=[]
nreviews_w_test=nreviews_test-len(r_del)
for i in range(nreviews_w_test):
    sen=document_re_test[i]
    txt=""
    for w in sen:
        txt=txt+w+" "
    text.append(txt)

data_w_test["text"]=text    
        
data_w_test.to_csv("test_cleaned.csv", sep=',', encoding="utf-8", index=0)
