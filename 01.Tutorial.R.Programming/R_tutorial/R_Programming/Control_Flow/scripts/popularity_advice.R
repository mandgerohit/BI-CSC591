# You're about to write popularity_advice() function! 


#
# Below you will create a function called popularity_advice. 
# It is similar to popularity_test(). But if the 'if- control statement does not hold,
# it appends a commentary/advice message. 
# This function returns the popularity test/advice results message.
# Be sure to save this script and type submit() in the console after you make your changes.

popularity_advice <- function(medium,views) {
  msg <- "Popularity Test Results: "
  my_medium <- medium
  num_views <- views
  
  # Examine the if-else statement for medium
  if(my_medium == "LinkedIn") {
     msg <- paste(msg, "Showing LinkedIn information")
  } else {
     msg <- paste(msg, "Unknown medium.")
  }
  
  # Assignment: Write the else statement for num_views
  if (num_views > 15) {
    msg <- paste(msg, "You're popular!")
  } 
  
  # Return popularity test result message
  msg
}
