#install.packages("cvTools")
library(cvTools)

data(iris)
dataframe <- iris
k = 10
error = c()

folds<-cvFolds(nrow(dataframe),10,type="random")

for(i in 1:k){
  trainindex <- which(folds$which==i)
  trainset <- dataframe[trainindex, ]
  testset <- dataframe[-trainindex, ]
  fit <- glm(Species ~ ., data = trainset, family = "binomial")
  predicted <- ifelse(predict(fit, testset, type="response")>.2, 1, 0)
  t <- table(predicted,testset$Species)
  error <- c(error, (t[2] + t[3])/ sum(t))
  #error[i] = (sum(t) - sum(diag(t)))/sum(t)
}

result <- t.test(error, alternative = "greater", mu = 0.1)
qqnorm(error)
print(result)
