#CARREGA AS BIBLIOTECAS PARA O TREINAMENTO
library(caret)
library(Rmpi) 
library(doMPI)

#CRIA CLUSTER PARA PARALELIZACAO DO JOB DE TREINAMENTO
cl <- startMPIcluster()
registerDoMPI(cl)

#CRIA OS DATAFRAMES
df <- read.csv("dataframe.csv")  #carrega arquivo de resultados, quando nao tiver SQL
df$clima <- NULL
df$tipologia <- NULL
df$caso <- NULL
df$ambiente <- NULL

df.aquec <- df[,-31]
df.aquec <- df.aquec[,-30]

df.aquec <- df.aquec[-(265001:725000),]
df.aquec <- df.aquec[-(165001:250000),]
df.aquec <- df.aquec[-(90001:150000),]
df.aquec <- df.aquec[-(15001:75000),]

#### Treinamento da RNA ####

#configuracoes de validacao cruzada
fitControl <- trainControl(method="repeatedcv", number = 3, repeats = 3)

#rede neural para consumo para aquecimento
nnetFit <- train( Aquec ~ .,
                  
                  data      = df.aquec,
                  preProc   = c("center", "scale"),
                  method    = "nnet", 
                  rang      = 1,
                  maxit     = 1e+7,
                  MaxNWts   = 3000,
                  abstol    = 0.1,
                  linout    = T,
                  trControl = fitControl,
                  tuneGrid  = expand.grid(.size=c(80),.decay=c(5e-4)))

save(nnetFit, file="aquecimento.rna")

closeCluster(cl)

mpi.finalize()
