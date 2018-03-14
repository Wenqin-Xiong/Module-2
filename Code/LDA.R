##Laten Dirichlet Allocation
#setwd("C:\\Users\\Ibara Jin\\Desktop\\伊原尋\\(学习)解読不能\\STAT628统计实习\\Module2")

# install.packages("ldatuning")
# install.packages("devtools")
# install.packages("topicmodels")
# install.packages("readr")
# install.packages("tokenizers")
# install.packages("tm")
# install.packages("ggplot2")
# install.packages("dplyr")
# install.packages("tidyr")
# install.packages("tidytext")
# 
# devtools::install_github("nikita-moor/ldatuning")

library("ldatuning")
library("topicmodels")
library("readr")
library("tokenizers")
library("tm")
library("topicmodels")
library("ggplot2")
library("dplyr")
library("tidyr")
library("tidytext")
library("zoo")


data=read_csv("data_cleaned.csv")

#nreviews=100000
nreviews=nrow(data)

dataLDA=data[1:nreviews,]
textLDA=dataLDA$text

document=list()
i=1
for(sen in textLDA){
  sen_vec=strsplit(sen, " ")
  sen_vec=unlist(sen_vec)
  if("neg_w" %in% sen_vec){
    sen_vec=sen_vec[-which(sen_vec=="neg_w")]
  }
  document[[i]]=sen_vec
  i=i+1
  if(i %% 1000 == 0){
    print(i)
  }
}

dict=unlist(document)
dict=table(dict)
dict=as.data.frame(dict)%>%
dict=dict %>%  
  arrange(desc(Freq))

index=c(1:1000)

Words.high=dict$dict[index]

document.high=list()
missing.ID=vector(mode="numeric",length = 0)
for(i in 1:nreviews){
  sen=document[[i]]
  sen=sen[which(sen %in% Words.high)]
  if(length(sen)==0){
    missing.ID=c(missing.ID,i)
  }else{
    document.high[[i]]=sen
  }
  if(i %% 1000 == 0){
    print(i)
  }
}

sample=sample(1:nreviews, 100000)
document.high=document.high[sample]

doc.corpus=Corpus(VectorSource(document.high))
dtm=DocumentTermMatrix(doc.corpus)

sen.len=apply(dtm,1,sum) #Find the sum of words in each Document
dtm=dtm[sen.len>0,] #remove all docs without words

#data("AssociatedPress", package="topicmodels")

topic.num = FindTopicsNumber(
  dtm,
  topics = seq(2, 15),
  metrics = c("Griffiths2004", "CaoJuan2009", "Arun2010", "Deveaud2014"),
  method = "Gibbs",
  control = list(seed=18),
  mc.cores = 8,
  verbose = TRUE
)
FindTopicsNumber_plot(topic.num)
#Load Topic models

#Run Latent Dirichlet Allocation (LDA) using Gibbs Sampling
#set burn in
burnin = 1000
#thin the spaces between samples
thin = 500
#set random starts at 5
nstart= 5
#use random integers as seed 
seed = list(6918,1300,314,65312471,384)
#set number of topics 
k = 15
#run the LDA model
topic.LDA = LDA(dtm ,k, method="Gibbs", control=list(nstart=nstart, seed=seed, burnin=burnin,
                                                     thin=thin, best=TRUE))

topic.coef=as.data.frame(t(topic.LDA@beta))
colname=c()
for(i in 1:k){
  colname=c(colname,paste0("Topic",i))
}
colnames(topic.coef)=colname

topic.coef=topic.coef %>%
  mutate(terms=topic.LDA@terms) %>%
  gather("Topic1", "Topic2", "Topic3",
         "Topic4", "Topic5", "Topic6",
         "Topic7", "Topic8", "Topic9",
         "Topic10", "Topic11", "Topic12",
         "Topic13", "Topic14", "Topic15",
         key = topic, value = beta) %>%
  mutate(beta=exp(beta)) %>%
  filter(beta > 0.001) %>%
  spread(key = topic, value = beta) %>%
  na.fill(fill=0)
topic.coef=as.data.frame(topic.coef)%>%
  mutate(log_ratio = 0)

topic.topwords=topic.coef%>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, desc(beta))

#Plot of Terms
topic.topwords=topic.topwords %>%
  transmute(topic, terms) %>%
  spread(topic, terms) %>%
  mutate(term = reorder(terms, beta)) %>%
  ggplot(aes(term, beta, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip()

topic.coef=topic.coef%>%
  filter()
  mutate(topic = paste0("Topic", topic)) %>%
  spread(topic, beta) %>%
  filter(Topic1 > .001 | Topic2 > .001) %>%
  mutate(log_ratio = log2(Topic2/Topic1))

dict.LDA=topic.coef$term

write.csv(topic.coef,file="LDAcoef")

doc.corpus.full=Corpus(VectorSource(document.high))
dtm.full=DocumentTermMatrix(doc.corpus.full)

#probabilities associated with each topic assignment
posterior(topic.LDA, dtm.full)