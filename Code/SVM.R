#install.packages("e1071")
library(readr)
library(e1071)

dtm_mat=as.matrix(dtm_train)
train=data.frame(dtm_mat)
train$STAR=cleaned_data$stars
train$t
model_svm=svm(STAR~.,data = train,scale = FALSE,type="C-classification",contrasts=FALSE)
y.testsvm=predict(model_svm, newdata = z.test)
y.testtran=predict(model_svm, newdata = train[-STAR])
layout(matrix(c(1,2),byrow = F))
plot(z.imputed$INTRDVX,ylim=c(50,200))
plot(y.pred)

write(y.pred,file = "predict_value",ncolumns = 1)


dtmidf_mat=as.matrix(dtm_tfidf)
train_idf=data.frame(dtmidf_mat)
