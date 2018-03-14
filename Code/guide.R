train2 <- read.table("data2.rdata")
train2$STAR=cleaned_data$stars
z.names <- names(train2)

role <- rep("n",length(z.names))

role[z.names %in% "STAR"] <- "d"

write("train2.rdata","train2dsc.txt")
write("NA",file="train2dsc.txt",append=TRUE)
write("2",file="train2dsc.txt",append=TRUE)
write.table(cbind(1:ncol(train2),names(train2),role),file="train2dsc.txt",append=TRUE,
            row.names=FALSE,col.names=FALSE,quote=FALSE)
write.table(train2,"train2.rdata",row.names = F,col.names = T)
