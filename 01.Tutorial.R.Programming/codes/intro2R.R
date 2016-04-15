# R code accompanying Introduction to R lecture slides

#--------------------------
# Building blocks in R
#--------------------------
lecture <- "Intro to R"
lec_no <- 1
big_data <- matrix (1:1000, nrow=100)

ls()
objects()

# You often want to remove objects
# to free up memory in your R environment
rm(big_data)
ls()
rm(list=ls())

demo()
demo(package = .packages(all.available = TRUE))
demo(graphics)

# check Values in Global Environment 
# under Environment tab on the right
ls()

#----------------------------------------
# Elements of R object: High-level
# names(), attributes(),
# class(), mode(), length(), typeof()
#----------------------------------------
demo(graphics)
# check pie.sales object is in the Environment
ls()
pie.sales
mode(pie.sales)
class(pie.sales)
names(pie.sales)
attributes(pie.sales)
typeof(pie.sales)
length(pie.sales)

rm(list=ls())
ls()

#---------------------------------
# mode(): how R object is STORED 
#  automic structures: numeric, complex, character, logical, raw
#  recursive structure: list 
#  advanced structures: function
#----------------------------------
a <- c("1","2")
b <- c(1,2)
c <- data.frame(1,2)
d <- plot
e<-1
f<-TRUE
mode(a)
mode(b)
mode(c)
mode(d)
mode(e)
mode(f)

#------------------------------------------
# Coercion: the change of the object's mode 
# > as.numeric(x)
# > as.list(x)
# > as.vector(x)
#   implicit vs explicit coercion
#   not every mode can be coerced to any other mode (incompatibility)
#   may result in distorted values (loss of precision)
#   not always reversible (irreversible)
#   may result in NA (missing values)
#-----------------------------------------
# NA introduced by coercion
z <- c("1","2","CISCO") 
mode(z)
y <- as.numeric(z)
y
mode(y)

# Incompatible coercion
df<-data.frame(x=1:3, y=4:6)
mode(df)
num <- as.numeric(df)
mode(num)
ls()

#----------------------
# mode() s. class()
#----------------------

x <- c(1:5)
y <- c(6:10)
fm <- lm(y ~ x)
class(fm)
mode(fm)
mode(lm)
class(lm)
plot(fm)

#-------------------------------------------------------------
# Data structures: vectors, matrices, arrays data frames, lists
# Note: Homogeneous Type: vectors (1D), matrices (2D), arrays (>2D)
#       Heterogenous Type: data frames, lists
#-------------------------------------------------------------
help.search("matrix")
help.search(matrix)

help("matrix")
help(matrix)
example(matrix) 

#=============================================
# Functions: Matching the class of the object 
# passed to a function as an argument
#---------------------------------------------
help(hist)
hist(x=rnorm(50),breaks=data.frame(-3,-2,-1,0,1,2,3),freq="yes")

my_x <- rnorm(50)
help(rnorm)
range(my_x)
my_breaks <- data.frame(-3,-2,-1,0,1,2,3)
my_freq <- "yes"
hist(x=my_x,breaks=my_breaks,freq=my_freq)
class(my_breaks)
class(my_freq)
class(my_x)

hist(x=my_x, breaks=c(-3,-2,-1,0,1,2,3), freq=TRUE)

#----------------------------------------
# Call a function: By its signature
# To check function's signature and usage:
#    help(function_name)
#    args(function_name)
#    example(function_name)
#----------------------------------------
x <- rnorm(10)
noise <- rnorm(10,mean=0, sd=0.1)
y<- 2*x + noise
my_data <- data.frame(x,y) 

help(lm)
args(lm)
# Run examples on the bottom of help(lm) page
example(lm)

lm(formula=y ~ x, data=my_data)
z <- lm(y ~ x, my_data)
z
summary(lm(y ~ x, data=my_data))

#-------------------------------
# Display R code for a function
#-------------------------------
mysum <- function (x1, x2) 
{
  return (x1+x2)
}
mysum

plot

lm

#------------------------------------
# Writing a function in another file
# and loading function into the environment
# with the source() command
#------------------------------------
rm (list=ls())
getwd()
source("functions.R")
ls()
myprod(3,5)
# see f() code
myprod

#---------------------------------------------------
# Returning a list of named objects from a function
#---------------------------------------------------
getwd()
source("functions.R")
mymath
result<-mymath(2,6)
class(result)
result

#-----------------------------------------
# Accessing objects in the list:
#   via $
#   via position # as a sublist
#   via position # as a value of the list object
#   via the name of the object in the list
#------------------------------------------
result<-mymath(2,6)
result
# via $
result$sum
result$product

# via position number as a sublist
result[1]
result[2]

# via position number as a value
result[[1]]
result[[2]]

# note differences in class() output
class(result[1])   # list
class(result[[1]]) # value type

# via object's name
result["sum"]   # list
result[["sum"]] # value
result['product'] # single quotes are OK
summary(result)

#------------------------------------
# Named functions arguments with
#   DEFAULT values
#------------------------------------
# reload R f()'s
source("functions.R")
ls()
mydiv(8,2)
# swap named args
mydiv(denominator=2, nominator=8)
# check division by 0
mydiv(5,0)
# default arg values
mydiv(denominator=2)
mydiv(nominator=5)

#====================================================
# Vectorization: pre-allocated vs re-allocated memory
#----------------------------------------------------
# Memory re-allocation is costly
obj <- c()
length(obj)
obj[5] <- 7  
length(obj)

# Pre-allocate memory to avoid re-allocation
help(rep)
# create a vector of 5 elements 
# with NA's as default values
obj <- rep(NA, 5) 
obj
length(obj) 
obj[5] <- 7  
length(obj)
obj

#------------------------------------------
# Vectorized operations with apply()-family
# Ex: For each vector element, 
# display its number of chars with nchar()
#------------------------------------------
vv <- c("I", "work", "at", "CISCO")
vv

# Option 1: A bad way of applying a function to
# each element of a vector
result <- c(nchar(vv[1]), nchar(vv[2]),
            nchar(vv[3]), nchar(vv[4]))

result

# Option 2: Use sapply()
help(sapply)
sapply(vv, nchar)

# Option 3: Check if the function is already vectorized,
# i.e., take vector as its argument,
# and simply pass a vector to the function
help(nchar)
nchar(vv)

#---------------------------------
# Vectorized operation on a matrix
# using apply() function
# Ex: Compute sum() for each row of the matrix
#----------------------------------
rm(list=ls())
v1 <- rep(1,4)
v2 <- rep(2,4)
v3 <- rep(3,4)
v3
AA <- rbind(v1,v2,v3)
help(rbind)
AA
AA[1,] 

# Option 1: Brute-force is BAD
# What if there are 1,000 rows?
result <- c(sum(AA[1,]),
            sum(AA[2,]), sum(AA[3,]))
result

# Option 2: Use apply()
apply(AA, 1, sum) # by row: 1
apply(AA, 2, sum) # by column: 2

#---------------------------------
# Vectorized operation on a matrix
# using apply() function
# Ex: Compute mean() for each column 
# of AA matrix
#----------------------------------
apply(AA, 2, mean) # by column: 2

#---------------------------------
# What if the function passed apply()
#   requires more than one argument?
# Ex: Compute inner_product() for each row 
# of AA matrix with vector b<-c(4,5,6)
#----------------------------------
source("functions.R")
inner_product
v1 <- c(1,2,3)
v2 <- c(2,3,4)

inner_product(v1,v2)

b<- c(4,5,6,7)
# computer inner product between 
# each row of AA and b
apply(AA, 1, inner_product, b) # by row: 1

# Check your solution using matrix multiplication
AA%*%as.matrix(b)

#--------------------------------------------
# Compute the sum() for each row of the matrix
#--------------------------------------------
source("functions.R")
ls()
mm <- matrix(c(1:8),nrow=2)
mm
matrixRowSums(mm)
vv <- c(1:8)
matrixRowSums(vv)
matrixRowSums(matrix(vv, ncol=length(vv)))

#----------------------------
# Vectorized operation on a list object
# using lapply() function
# Note: it is lapply() not apply()
# Ex: Compute mean() for each object in the list
#----------------------------
rm(list=ls())

vv <- c(1:10)
beta <- exp(-3:3)
ll <- c(TRUE, FALSE, FALSE)
my_list <- list(v=vv, b=beta, l=ll)
my_list
class(my_list)
lapply(my_list, mean)



