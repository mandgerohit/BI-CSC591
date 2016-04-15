source("functions.R")
df <- data.frame(c(1:4),c(5:8))
class(df) 
mode(df)
mm <- as.matrix(df) # coerce to matrix
class(mm)
mode(mm)
dim(mm)
mm
matrixRowSums(mm)
