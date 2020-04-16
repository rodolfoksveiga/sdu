#CARREGA AS BIBLIOTECAS PARA O TREINAMENTO
library(caret)
library(Rmpi) 
library(doMPI)

df <- read.csv("floripa_conforto_new.csv")

#REORDER RESULTS COLUMN
movetolast <- function(data, move) {data[c(setdiff(names(data), move), move)]}
df <- movetolast(df, c("Phoras"))
df<- subset(df, df$small_opening_area ==0)

df$clima <- df$tipologia <- df$id_caso <- df$ambiente <- NULL
df$ter_wall_area <- df$ter_wall_ori <- df$small_opening_area <- df$small_opening_ori <- NULL
df$sec_wall_area <- df$exp_cob <- df$a_par_int <- df$area_util <- NULL
df <- df[sample(nrow(df), size = 100000, replace = FALSE),]

#### Treinamento da RNA ####
cl <- startMPIcluster()
registerDoMPI(cl)

#configuracoes de validacao cruzada
fitControl <- trainControl(method="repeatedcv", number = 6, repeats = 6)

#rede neural para consumo para aquecimento
nnetFit <- train( Phoras ~ .,
                  
                  data      = df,
                  preProc   = c("center", "scale"),
                  method    = "nnet", 
                  rang      = 1,
                  maxit     = 1e+7,
                  MaxNWts   = 3000,
                  abstol    = 0.1,
                  linout    = T,
                  trControl = fitControl,
                  tuneGrid  = expand.grid(.size=c(120),.decay=c(5e-4)))

save(nnetFit, file="floripa_phoras_final.rna")

closeCluster(cl)

mpi.finalize()

