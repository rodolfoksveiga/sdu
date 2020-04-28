import glob
import os
import csv
import shutil
import sys
import codecs

def writeFinalValues(row):
	testFileAndWriteHeader()
	csvOut = open('resumoerros.csv', 'a', encoding='iso-8859-1')
##	csvOut = open('resumoerros.csv', 'a')
	csvWriter = csv.writer(csvOut, delimiter=',')
	csvWriter.writerow(row)
	csvOut.close()

def testFileAndWriteHeader():
	if not os.path.isfile('resumoerros.csv'):
		header = ['Case', 'SevereCompleted', 'SevereSizing', 'SevereWarmup', 'WarningsCompleted']
		header += ['WarningsSizing', 'WarningsWarmup']		
		csvOut = open('resumoerros.csv', 'a', encoding='iso-8859-1')
##		csvOut = open('resumoerros.csv', 'a')
		csvWriter = csv.writer(csvOut, delimiter=',')
		csvWriter.writerow(header)
		csvOut.close()

case = list(sys.argv)[1]
if not case.endswith('/'):
	case += '/'

nomeArquivoGrupoErro = case + 'eplusout.err'

dadoArquivoGrupoErro = open(nomeArquivoGrupoErro, 'r', encoding='iso-8859-1')
dadoArquivoGrupoErro = dadoArquivoGrupoErro.readlines()


for i in dadoArquivoGrupoErro:
	if "************* EnergyPlus Warmup Error Summary" in i:
		WarningWarmup=(i[i.find(": ")+2:i.find("Warning;")-1]) 
		SevereWarmup=(i[i.find("; ")+2:i.find("Severe")-1])
	if "************* EnergyPlus Sizing Error Summary" in i:
		WarningSizing=(i[i.find(": ")+2:i.find("Warning;")-1])
		SevereSizing=(i[i.find("; ")+2:i.find("Severe")-1])
	if "************* EnergyPlus Completed Successfully--" in i:
		WarningCompleted=(i[i.find('-- ')+3:i.find(' Warning;')])
		SevereCompleted=(i[i.find("; ")+2:i.find(" Severe")])


## Creates the row that will be written in the csv.
row = [os.path.basename(os.path.normpath(case)), SevereCompleted, SevereSizing, SevereWarmup, WarningCompleted, WarningSizing, WarningWarmup]


## Writes the row in the 'resultado.csv' file.
writeFinalValues(row)




