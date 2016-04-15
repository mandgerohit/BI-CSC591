#----------------------------------------------
# Avoid loops!!!
# Check how the same functionality
# is implemented using apply() in
# matrixRowsSums() function in functions.R
#----------------------------------------------
avoidLoops <- function(data) 
{
  if (is.matrix(data) == TRUE) {
    sums <- c()
    for ( rindex in 1:nrow(data) ) {
      rowSum <- sum(data[rindex, ])
      sums <- c(sums, rowSum)
    } 
    return (sums)
  }
  else return (NULL)
}
