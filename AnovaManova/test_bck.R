
#data <- read.table("http://www.umass.edu/statdata/statdata/data/aps.dat", quote="\"", comment.char="")
#Randomly shuffle the data
#dataframe<-data[sample(nrow(data)),]
data(iris)
nrow(iris)
head(iris)
dataframe <- iris
k = 10
error = c()

for(i in 1:k){
  index <- 1:nrow(dataframe)
  trainindex <- sample(index, trunc(length(index)/2))
  trainset <- dataframe[trainindex, ]
  testset <- dataframe[-trainindex, ]
  fit <- glm(Species ~ ., data = trainset, family = "binomial")
  predicted <- ifelse(predict(fit, testset, type="response")>.2, 1, 0)
  t <- table(predicted,testset$Species)
  error <- c(error, (t[2] + t[3])/ sum(t))
  #error[i] = (sum(t) - sum(diag(t)))/sum(t)
}

m = mean(error)
var = var(error)
result <- t.test(error, alternative = "greater", mu = 0.15)
qqnorm(error)

require (ggplot2)
ggplot(data.frame(x=error)) +
  geom_density(aes(x=x), fill="grey", color="grey") +
  geom_vline(xintercept=result$statistic, color="red") +
  geom_vline(xintercept=mean(error) +
               c(-2,2)*sd(error), linetype=2)