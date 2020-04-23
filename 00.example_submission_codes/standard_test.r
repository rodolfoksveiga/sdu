#### TREINAMENTO DA REDE ####
library(caret)
library(Rmpi)
library(doMPI)

cl <- startMPIcluster()
registerDoMPI(cl)

df <- read.csv("tratamento.csv")  #carrega arquivo de resultados
df.aquec <- df[,-30]
df.resfr <- df[,-29]

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

save(nnetFit, file="aquecimento2.rna")

#rede neural para consumo para resfriamento
nnetFit <- train( Resfr ~ .,
                  
                  data      = df.resfr,
                  preProc   = c("center", "scale"),
                  method    = "nnet", 
                  rang      = 1,
                  maxit     = 1e+7,
                  MaxNWts   = 3000,
                  abstol    = 0.1,
                  linout    = T,
                  trControl = fitControl,
                  tuneGrid  = expand.grid(.size=c(80),.decay=c(5e-4)))

save(nnetFit, file="resfriamento2.rna")

closeCluster(cl)

mpi.finalize()

