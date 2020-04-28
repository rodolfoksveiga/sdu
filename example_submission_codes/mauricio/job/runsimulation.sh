#!/bin/sh

now=$(date +"%T")
echo Iniciando $1 - $now >> $2

cd $1

cp /scratch/prjeeesd/roberto.lamberts/banco1/arquivos/Energy+.idd Energy+.idd

cp in0.idf in.idf
ExpandObjects in.idf
mv expanded.idf in.idf

energyplus

ReadVarsESO

cd ../resultados
python erros.py $1
python resultados.py $1

now=$(date +"%T")
echo Finalizando $1 - $now >> $2
