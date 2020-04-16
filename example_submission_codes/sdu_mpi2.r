### Separacao dos dataframes ####

library(caret)
library(Rmpi)
library(doMPI)

df <- read.csv("tratamento.csv")  #carrega arquivo de resultados
df.aquec <- df[,-31]
df.aquec <- df.aquec[,-30]

df.resfr <- df[,-31]
df.resfr <- df.resfr[,-29]

df.tempo <- df[,-30]
df.tempo <- df.tempo[,-29]

cl <- startMPIcluster()
registerDoMPI(cl)

#### Treinamento das RNAs ####

#configuracoees de validacao cruzada
fitControl <- trainControl(method="repeatedcv", number = 8, repeats = 6)

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

save(nnetFit, file="resfriamento.rna")

#rede neural para consumo para conforto
nnetFit <- train( Phoras ~ .,

                  data      = df.tempo,
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

