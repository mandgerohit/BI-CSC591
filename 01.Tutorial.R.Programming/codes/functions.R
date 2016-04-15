#-------------------------------------
# It is a good habit to keep functions
# in a separate file that you can reuse
# across different R codes by using 
# source("file_name") command in R code
#-------------------------------------
myprod <- function (x, y) 
{
  product <- x * y 
  return (product)
}

#----------------------------
# Returning named objects
#  from a function
# NOTE: You musr create a list
# object with list() 
# to return more than one
# object from a function
#----------------------------
mymath <- function (x, y) 
{
  multiplication <- x * y
  addition <- x + y 
  output <- list(sum=addition,
                 product = multiplication) 
  return (output)
}

#------------------------------------
# Named functions arguments with
#   DEFAULT values
#-----------------------------------
mydiv <- function(nominator=1, denominator=1) 
{
  div <- NA
  error <- "OK"
  if (denominator == 0) 
  { error <- "Division by zero" }
  else { div <- nominator/denominator }
  output <- list(division=div, status = error) 
  return (output)
}

#------------------------------------------------
# Function that computes an inner/scalar product 
# of two vectors.
# Is this a vectorized function?
# -----------------------------------------------
inner_product <- function(rowvec, colvec) 
{
  inner <- NA
  if(length(rowvec) == length(colvec)) {
    product <- rowvec * colvec 
    inner <- sum(product)
  }
  
  return (inner)
}

#-----------------------------------
# A function that uses apply() 
# and returns the sum of row elements
# in a matrix passed as an argument
#-----------------------------------
matrixRowSums <- function(data) 
{
  if (is.matrix(data) == TRUE) {
    margin = 1 # summing by rows
    sums <- apply (data, margin, sum)
    return (sums)
  }
  else {
    print("ERROR: argument must be a matrix")
    return (NA)
  }
}

