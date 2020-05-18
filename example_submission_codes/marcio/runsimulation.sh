#!/bin/sh

now=$(date +"%T")
echo Iniciando $1 - $now >> $2

cd $1

cp /scratch/prjeeesd/leonardo.mazzaferro/salvador/arquivos/Energy+.idd Energy+.idd
cp /scratch/prjeeesd/leonardo.mazzaferro/salvador/arquivos/in.epw in.epw
cp /scratch/prjeeesd/leonardo.mazzaferro/salvador/arquivos/Conforto.csv Conforto.csv

ExpandObjects in.idf
mv expanded.idf in.idf

energyplus

ReadVarsESO

cd ../resultados
python resultados.py $1

now=$(date +"%T")
echo Finalizando $1 - $now >> $2
