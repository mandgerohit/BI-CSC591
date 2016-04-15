# Load the libraries 
#install.packages("vars")
#install.packages("tseries")
#install.packages("stats")
#install.packages("pcalg")
library(vars)
library(tseries)
library(stats)
library(pcalg)
library(igraph)

# Read the input data 
data = read.csv("/home/rnmandge/BI/CausalRelationDiscovery/InputData/data.csv", header = TRUE)

# Build a VAR model 
t_var <- VAR(data, type = c("const"),ic = c("SC"))

# Extract the residuals from the VAR model 
t_res <- residuals(t_var)
t_res <- as.ts(t_res)
is.ts(t_res)

# Check for stationarity using the Augmented Dickey-Fuller test 
adf.test(t_res[,1], alternative = "stationary", k=0)
adf.test(t_res[,2], alternative = "stationary", k=0)
adf.test(t_res[,3], alternative = "stationary", k=0)

# Check whether the variables follow a Gaussian distribution 
ks.test(t_res[,1],"pnorm")
ks.test(t_res[,2],"pnorm")
ks.test(t_res[,3],"pnorm")

# Write the residuals to a csv file to build causal graphs using Tetrad software
write.csv(t_res, file = "/home/rnmandge/BI/CausalRelationDiscovery/residuals.csv", row.names = FALSE)

# Read residuals
g_data <- read.csv("/home/rnmandge/BI/CausalRelationDiscovery/residuals.csv", header = TRUE)
rows <- nrow(g_data)

############# PC Algorithm
suffStat=list(C=cor(g_data),n=rows)
pc_fit <- pc(suffStat, indepTest=gaussCItest, alpha=0.1, labels=colnames(g_data), skel.method="original", verbose=TRUE)
plot(pc_fit, main="PC Output")

############ LiNGAM Algorithm
lingam_fit <- LINGAM(g_data, verbose=TRUE)
show(lingam_fit)
rownames(lingam_fit$Adj)=c("MOVE", "RPRICE", "MPRICE")
colnames(lingam_fit$Adj)=c("MOVE", "RPRICE", "MPRICE")
plot(graph.adjacency(lingam_fit$Adj, mode="directed"))
