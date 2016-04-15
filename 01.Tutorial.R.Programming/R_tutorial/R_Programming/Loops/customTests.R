test_func1 <- function() {
  try({
    func <- get('for_by_element', globalenv())
    t1 <- identical(func(), " 1 2 3")
    t2 <- identical(func(4), " 1 2 3 4")
    t3 <- identical(func(2), " 1 2")
    ok <- all(t1, t2, t3)
  }, silent = TRUE)
  exists('ok') && isTRUE(ok)
}

test_func2 <- function() {
  try({
    func <- get('for_by_position', globalenv())
    t1 <- identical(func(), "3 2 1 ")
    t2 <- identical(func(4), "4 3 2 1 ")
    t3 <- identical(func(2), "2 1 ")
    ok <- all(t1, t2, t3)
  }, silent = TRUE)
  exists('ok') && isTRUE(ok)
}

test_func3 <- function() {
  try({
    func <- get('for_over_list', globalenv())
    t1 <- identical(func(), list(element=sum(c(1:2))+sum(rep(1,2)),position=sum(c(1:2))+sum(rep(1,2))))
    t2 <- identical(func(3), list(element=sum(c(1:3))+sum(rep(1,3)),position=sum(c(1:3))+sum(rep(1,3))))
    t3 <- identical(func(2), list(element=sum(c(1:2))+sum(rep(1,2)),position=sum(c(1:2))+sum(rep(1,2))))
    ok <- all(t1, t2, t3)
  }, silent = TRUE)
  exists('ok') && isTRUE(ok)
}

test_func4 <- function() {
  try({
    func <- get('nested_for', globalenv())
    A <- matrix(c(1:16), nrow=4)
    B <- matrix(rep(1,16), nrow=4)
    t1 <- identical(as.numeric(func(A)),as.numeric(sum(A)))
    t2 <- identical(as.numeric(func(B)),as.numeric(sum(B)))
    ok <- all(t1, t2)
  }, silent = TRUE)
  exists('ok') && isTRUE(ok)
}

test_func5 <- function() {
  try({
    func <- get('while_stocks', globalenv())
    t1 <- identical(func(20), 0)
    t2 <- identical(func(30), 1)
    t3 <- identical(func(35), 2)
    ok <- all(t1, t2, t3)
  }, silent = TRUE)
  exists('ok') && isTRUE(ok)
}
