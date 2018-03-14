# training data
library(readr)
cleaned_data <- read_csv("data_cleaned.csv")
cleaned_data$X1=NULL
dim(cleaned_data)

# text2vec
library(text2vec)
prep_fun = tolower  
tok_fun = word_tokenizer
it_train = itoken(cleaned_data$text, preprocessor = prep_fun, tokenizer = tok_fun, ids = cleaned_data$name, progressbar = FALSE)
vocab = create_vocabulary(it_train)
vocab
library(dplyr)
train_tokens = cleaned_data$text %>% 
  prep_fun %>% 
  tok_fun
it_train = itoken(train_tokens, ids = cleaned_data$name,progressbar = FALSE)
vocab = create_vocabulary(it_train)
# delete low frequent words
pruned_vocab = prune_vocabulary(vocab, term_count_min = 1000,doc_proportion_max = 0.5,doc_proportion_min = 0.001)
pruned_vocab

# look at highest 50 frequently used words
u=length(pruned_vocab)
l=length(pruned_vocab)-50
hiest= pruned_vocab$term[l:u]

# change to vector, create sparse matrix and change to data frame
vectorizer = vocab_vectorizer(pruned_vocab)
dtm_all = create_dtm(it_train, vectorizer)
dim(dtm_all)
dtm= as.matrix(dtm_all)
data_train=data.frame(dtm)

# stars and city
library(readr)
train_data <- read_csv("train_data.csv")
STARS= train_data$stars
CITY= as.factor(train_data$city)

# length of text
LENGTH=1:1546379
text= train_data$text
for (i in 1:1546379){
  txt=text[i]
  D=as.character(txt)
  Y=strsplit(D," ")
  LENGTH[i]=length(Y[[1]])
}
length(LENGTH)

# plot stars vs. length 

id1=which(train$stars==1)
id2=which(train$stars==2)
id3=which(train$stars==3)
id4=which(train$stars==4)
id5=which(train$stars==5)

d1= train$text[id1]
d2= train$text[id2]
d3= train$text[id3]
d4= train$text[id4]
d5= train$text[id5]

avg_num_wd=1:5

lg=1:length(d1)
for (i in 1:length(d1)){
  txt=d1[i]
  D=as.character(txt)
  Y=strsplit(D," ")
  lg[i]=length(Y[[1]])
}
avg_num_wd[1]=mean(lg)

lg=1:length(d2)
for (i in 1:length(d2)){
  txt=d2[i]
  D=as.character(txt)
  Y=strsplit(D," ")
  lg[i]=length(Y[[1]])
}
avg_num_wd[2]=mean(lg)

lg=1:length(d3)
for (i in 1:length(d3)){
  txt=d3[i]
  D=as.character(txt)
  Y=strsplit(D," ")
  lg[i]=length(Y[[1]])
}
avg_num_wd[3]=mean(lg)

lg=1:length(d4)
for (i in 1:length(d4)){
  txt=d4[i]
  D=as.character(txt)
  Y=strsplit(D," ")
  lg[i]=length(Y[[1]])
}
avg_num_wd[4]=mean(lg)

lg=1:length(d5)
for (i in 1:length(d5)){
  txt=d5[i]
  D=as.character(txt)
  Y=strsplit(D," ")
  lg[i]=length(Y[[1]])
}
avg_num_wd[5]=mean(lg)

avg_num_wd

ratings=c(1,2,3,4,5)

dp=data.frame(ratings,avg_num_wd,row.names = NULL)

plot(dp,type = "h", col = "red", lwd = 10)

## tf-idf
library(text2vec)
tfidf = TfIdf$new()
dtm_train_tfidf = fit_transform(dtm_train, tfidf)


