#CARREGA AS BIBLIOTECAS PARA O TREINAMENTO
library(caret)
library(Rmpi) 
library(doMPI)

#CRIA CLUSTER PARA PARALELIZACAO DO JOB DE TREINAMENTO
cl <- startMPIcluster()
registerDoMPI(cl)

#CRIA OS DATAFRAMES
#setwd("C:/Users/leonardo.mazzaferro/Dropbox/ns_rtqr/gustavo")
df <- read.csv("dataframe.csv")  #carrega arquivo de resultados, quando nao tiver SQL
df$clima <- NULL
df$tipologia <- NULL
df$caso <- NULL
df$ambiente <- NULL

df.aquec <- df[,-31]
df.aquec <- df.aquec[,-30]

df.resfr <- df[,-31]
df.resfr <- df.resfr[,-29]

df.conf <- df[,-30]
df.conf <- df.conf[,-29]

#### Treinamento da RNA ####

#configurações de validação cruzada
fitControl <- trainControl(method="repeatedcv", number = 3, repeats = 3)

#rede neural para consumo para conforto
nnetFit <- train( Phoras ~ .,                  
                  data      = df.conf,
                  preProc   = c("center", "scale"),
                  method    = "nnet", 
                  rang      = 1,
                  maxit     = 1e+7,
                  MaxNWts   = 3000,
                  abstol    = 0.1,
                  linout    = T,
                  trControl = fitControl,
                  tuneGrid  = expand.grid(.size=c(80),.decay=c(5e-4)))

save(nnetFit, file="conforto.rna")

closeCluster(cl)

mpi.finalize()
