# You're about to examine more else-if-else statements in R! 

# Do NOT edit this script; simply type submit() in the console after you examine it.

else_if_numeric_test <- function(number) {
  msg <- "Number: "

  if(number < 10) {
    if(number < 5) {
      msg <- paste(msg,"extra small")
    } else {
      msg <- paste(msg,"small")
    }
  } else if (number < 100) {
    msg <- paste(msg,"medium")
  } else {
    msg <- paste(msg,"large")
  }
  
  # Return popularity test result message
  msg
}
