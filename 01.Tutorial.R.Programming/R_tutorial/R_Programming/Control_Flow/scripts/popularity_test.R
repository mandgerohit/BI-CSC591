# You're about to write popularity_test function! 

# Remind that just like you would assign a value 
# to a variable with the assignment operator, you assign functions in the following
# way:
#
# function_name <- function(arg1, arg2){
#	# Manipulate arguments in some way
#	# Return a value
# }
#
# The "variable name" you assign will become the name of your function. arg1 and
# arg2 represent the arguments of your function. You can manipulate the arguments
# you specify within the function. After sourcing the function, you can use the 
# function by typing:
# 
# function_name(value1, value2)
#
# Below you will create a function called popularity_test. This function takes
# two arguments as input, and returns the popularity test results message.
# Be sure to save this script and type submit() in the console after you make your changes.

popularity_test <- function(medium,views) {
  msg <- "Popularity Test Results: "
  my_medium <- medium
  num_views <- views
  
  # Examine the if statement for medium
  if(my_medium == "LinkedIn") {
    msg <- paste(msg, "Showing LinkedIn information")
  }
  
  # Assignment: Write the if statement for num_views
  
  
  # Return popularity test result message
  msg
}
