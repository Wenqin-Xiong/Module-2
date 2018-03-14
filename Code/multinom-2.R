data_full <- read.table("data_full.rdata",header = T)
#lm_city <- lm(STARS~CITY,data = data_full)

data_full$STARS <- as.factor(data_full$STARS)
lm_voca <- lm(as.numeric(data_full$STARS)~.,data = data_full[,c(-1001,-1002)])
sum1 <- summary(lm_voca)
order_p <- order(sum1$coefficients[,4],decreasing = F)
print(sum1$coefficients[order_p[2:181],])
voca_name <- row.names(sum1$coefficients[order_p[2:181],])

data_fit <- data_full[,voca_name]
data_fit$LENGTH <- data_full$LENGTH
data_fit$STARS <- data_full$STARS

# Model fitting
# install.packages("nnet")
library("nnet")
multinom1 <- multinom(STARS~.,data = data_fit)
#summary1=summary(multinom1)

# Predict by class
pred1 <- data_fit[,-182]
p1 <- predict(multinom1, pred1, type = "class")

obs <- data_full$STARS
summary(obs)

# Accuracy
count <- 0
for (i in 1:length(p1)){
  if (p1[i]==obs[i]){
    count <- count+1
  }
}

# MSE
pred_num=as.numeric(p1)
obs_num=as.numeric(data_full$STAR)
sum_1=c()
for (i in 1:length(pred_num)){
  sum_1[i]=(pred_num[i]-obs_num[i])^2
}
mean(sum_1)

# Predict by probs
p2 <- predict(multinom1, pred1, type = "probs")
str(p2)
result <- c()
for (i in 1:dim(p2)[1]){
  index <- order(p2[i,],decreasing = T)[1:5]
  result[i] <- sum(p2[i,index]/sum(p2[i,index])*index)
}
summary(result)

# MSE
sum_2 <- c()
for (i in 1:length(result)){
  sum_2[i] <- (result[i]-obs_num[i])^2
}
mean(sum_2)

# Prediction for test data
#library(readr)
#data_test <- read_csv("test_cleaned.csv")

