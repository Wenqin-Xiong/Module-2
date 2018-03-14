# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 17:38:53 2018

@author: Ibara Jin
"""

data_debug = pandas.read_csv('data_cleaned.csv',index_col=0, encoding='iso-8859-1')
freq_std = pandas.read_csv('frequency.csv')

freq_std=freq_std[freq_std.word != "never"]
freq_std=freq_std[freq_std.word != "cannot"]
freq_std=freq_std[freq_std.word != "dont"]

data_txt=data_debug["text"]
r_del=[]
document_re=[]
nreviews=data_debug.shape[0]
for i in range(nreviews):
    sen=data_txt[i]
    if type(sen)!=str:
        r_del.append(i)
    else:
        sen=sen.replace('cannot', "neg_w")
        sen=sen.replace('never', "neg_w")
        sen=sen.replace('dont', "neg_w")
        document_re.append(sen.split(" "))
        
freq_re=set(list(freq_std["word"]))
freq_re.add("neg_w")

data_w=data_debug.drop(r_del)
document_re=[[word for word in sen if word in freq_re] for sen in document_re]
 
data_w=data_w.drop("text", axis=1)
text=[]
nreviews_w=data_debug.shape[0]-len(r_del)
for i in range(nreviews_w):
    sen=document_re[i]
    txt=""
    for w in sen:
        txt=txt+w+" "
    text.append(txt)

data_w["text"]=text    
        
data_w.to_csv("data_cleaned.csv", sep=',', encoding="utf-8", index=0)
freq_std.to_csv("frequency.csv", sep=',', encoding="utf-8", index=0)

with open('document_re.csv', 'w', newline="") as myfile:
    writer = csv.writer(myfile)
    writer.writerows(document_re)

data_verify = pandas.read_csv('test_cleaned.csv')
nreviews_verify=data_verify.shape[0]

lon=data_test["longitude"]
lat=data_test["latitude"]
lon_verify=data_verify["longitude"]
lat_verify=data_verify["latitude"]

k=0
missing=[]
for i in range(nreviews_verify):
    if (lon[i+k]-lon_verify[i])>0.001 or (lat[i+k]-lat_verify[i])>0.001:
        missing.append(i+k)
        k=k+1
        
print(k)

#missing=[15379,48001,54805,71416,72087,199176,223042,228762,349705,376119,445509,447939,727005,738464,749039,959813,967963,971995]

text=list(data_verify["text"])
for i in missing:
    text.insert(i,"NA")

data_test_re=copy.deepcopy(data_test)
data_test_re["text"]=text

for i in missing:
    print(i)
    print(data_test["text"][i])
    print(data_test_re["text"][i])

data_test_re.to_csv("test_cleaned_re.csv", sep=',', encoding="utf-8", index=0)