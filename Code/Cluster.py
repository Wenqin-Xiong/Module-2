# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 23:39:34 2018

@author: wxiong29
"""
data=pandas.read_csv('data_cleaned.csv')  
nreviews=data.shape[0]
score=data["stars"]

with open("document_re.csv", 'r') as filein: 
    reader = csv.reader(filein)
    document_re = list(list(rec) for rec in csv.reader(filein, delimiter=',')) 
    
sentdict=pandas.read_csv('SentiDict_iter.csv')
sentdict=sentdict[abs(sentdict["sent"])>0.25]
sentdict=dict(zip(sentdict["word"],sentdict["sent"]))

sentiment=[]
i=0
for sen in document_re:
    flag=1
    senti=0
    if len(sen)>0:
        for word in sen:
            if word=="neg_w":
                flag=-1
            else:
                if word in sentdict:
                    senti+=sentdict[word]*flag
                    if flag==-1:
                        flag=1
        senti=senti/len(sen)
    sentiment.append(senti)
    i+=1
    if i % 10000 == 0:
        print(i)

from gensim import corpora, models, similarities
from gensim.test.utils import common_corpus, common_dictionary, get_tmpfile
from gensim.models import LsiModel

document=[[word for word in sen if word!="neg_w"] for sen in document_re]

dictLSI=corpora.Dictionary(document)
document_corpus=[dictLSI.doc2bow(sen) for sen in document]

tf_idf = models.TfidfModel(document_corpus)
document_tf_idf=tf_idf[document_corpus]
LSI = models.LsiModel(document_tf_idf, id2word=dictLSI, num_topics=15)
LSI.save('LSI.lsi') 

data_test=pandas.read_csv('test_cleaned_re.csv')
text_test=data_test["text"]
document_test=[]
for sen in text_test:
    if type(sen)==str:
        document_test.append(sen.split())
    else:
        document_test.append([])
        
with open('document_test.csv', 'w', newline="") as myfile:
    writer = csv.writer(myfile)
    writer.writerows(document_test)

document_test=document_re[0:10000]
 
index=list(range(nreviews))
rule=pandas.DataFrame({"index":index,"sen":sentiment,"score":score})
group=rule.groupby(by=np.round(rule.sen,2))
rule_re=group.mean()
rule_re=dict(zip(np.round(rule_re.sen,2),rule_re.score))

score_test=[]
i=0
for sen in document_test:
    senti=0
    for word in sen:
        if word in sentdict:
            senti=senti+sentdict[word]
    if len(sen)>0:
        senti=senti/len(sen)
        senti=round(senti,2)
        if senti < -0.7:
            score_test.append(1)
        elif senti > 0.84:
            score_test.append(5)
        else:
            score_test.append(rule_re[senti])
    else:
        score_test.append(5)
    i=i+1
    if i % 10000 == 0:
        print(i)
        
(sum((score[0:nreviews]-score_test)**2)/nreviews)**0.5

sims = similarities.MatrixSimilarity(LSI[document_tf_idf])
sims.save('LSI.index')

sims = similarities.MatrixSimilarity.load('LSI.index')

score_test=[]
i=0
for sen in document_test:
    if len(sen)>0:
        sen_corpus=dictLSI.doc2bow(sen)
        sen_vec=LSI[sen_corpus] 
        sims_sen=sims[sen_vec]
        sims_sen=sorted(enumerate(sims_sen), key=lambda item: -item[1])
        score_sen=0
        weight_sen=0
        for sen_alike in sims_sen[:10]:
            score_sen+=score[sen_alike[0]]*(sen_alike[1]+1)
            weight_sen+=(sen_alike[1]+1)
        score_test.append(score_sen/weight_sen)
    else:
        score_test.append(5)
    i=i+1
    if i % 10 == 0:
        print(i)
        
index_test=list(range(1,nreviews_test+1))

data_w=pandas.DataFrame({"Id":index_test,"Prediction1":score_test})
data_w.to_csv("predict.csv", sep=',', encoding="utf-8", index=0)
    