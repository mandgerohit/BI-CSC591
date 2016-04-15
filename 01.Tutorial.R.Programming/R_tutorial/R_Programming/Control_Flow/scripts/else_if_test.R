# You're about to write else-if control statement! 

# Be sure to save this script and type submit() in the console after you make your changes.

else_if_test <- function(medium,views) {
  msg <- "Popularity Test Results: "
  my_medium <- medium
  num_views <- views
  
  # Examine the if-else statement for medium
  if(my_medium == "LinkedIn") {
     msg <- paste(msg, "Showing LinkedIn information")
  } else if (medium == "Twitter") {
    msg <- paste(msg, "Showing Twitter information")
  } else {
     msg <- paste(msg, "Unknown medium.")
  }
  
  # Assignment: Write the else-if-else statement for num_views
  if (num_views > 15) {
    msg <- paste(msg, "You're popular!")
  } 
  
  # Return popularity test result message
  msg
}
