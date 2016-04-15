test_func1 <- function() {
  try({
    func <- get('popularity_test', globalenv())
    t1 <- identical(func("LinkedIn",16), paste("Popularity Test Results: ", "Showing LinkedIn information","You're popular!"))
    t2 <- identical(func("Facebook",16), paste("Popularity Test Results: ", "You're popular!"))
    t3 <- identical(func("LinkedIn",10), paste("Popularity Test Results: ", "Showing LinkedIn information"))
    ok <- all(t1, t2, t3)
  }, silent = TRUE)
  exists('ok') && isTRUE(ok)
}

test_func2 <- function() {
  try({
    func <- get('popularity_advice', globalenv())
    t1 <- identical(func("LinkedIn",16), paste("Popularity Test Results: ", "Showing LinkedIn information","You're popular!"))
    t2 <- identical(func("Facebook",16), paste("Popularity Test Results: ", "Unknown medium.", "You're popular!"))
    t3 <- identical(func("LinkedIn",10), paste("Popularity Test Results: ", "Showing LinkedIn information", "Try to be more visible!"))
    ok <- all(t1, t2, t3)
  }, silent = TRUE)
  exists('ok') && isTRUE(ok)
}

test_func3 <- function() {
  try({
    func <- get('else_if_test', globalenv())
    t1 <- identical(func("LinkedIn",16), paste("Popularity Test Results: ", "Showing LinkedIn information","You're popular!"))
    t2 <- identical(func("Facebook",16), paste("Popularity Test Results: ", "Unknown medium.", "You're popular!"))
    t3 <- identical(func("Twitter",14), paste("Popularity Test Results: ", "Showing Twitter information", "Your number of views is average"))
    ok <- all(t1, t2, t3)
  }, silent = TRUE)
  exists('ok') && isTRUE(ok)
}  

test_func4 <- function() {
  try({
    func <- get('else_if_numeric_test', globalenv())
    t1 <- identical(func(6), paste("Number: ", "small"))
    t2 <- identical(func(10), paste("Number: ", "medium"))
    t3 <- identical(func(4), paste("Number: ", "extra small"))
    ok <- all(t1, t2, t3)
  }, silent = TRUE)
  exists('ok') && isTRUE(ok)
}  

test_func5 <- function() {
  try({
    func <- get('control_actions', globalenv())
    t1 <- identical(func(15,9), 24)
    t2 <- identical(func(15,25), 80)
    t3 <- identical(func(5,10), 15)
    ok <- all(t1, t2, t3)
  }, silent = TRUE)
  exists('ok') && isTRUE(ok)
}  
