from __future__ import division
import os
import shutil
import csv
import tarfile
import sys


## Classe Casa, lista de ambientes

casas = []


class Casa:

	def __init__(self, casa):
		self.casa = casa
		self.ambientes = []
		self.ambientes.append(Ambiente("UH1DORM1", 3, 34, 48, 62, 20))
                self.ambientes.append(Ambiente("UH1DORM2", 3, 35, 49, 63, 21))
                self.ambientes.append(Ambiente("UH1SALA", 2, 36, 50, 64, 22))
		self.ambientes.append(Ambiente("UH2DORM1", 3, 38, 52, 66, 24))
                self.ambientes.append(Ambiente("UH2DORM2", 3, 37, 51, 65, 23))
                self.ambientes.append(Ambiente("UH2SALA", 2, 39, 53, 67, 25))
		self.ambientes.append(Ambiente("UH3DORM1", 3, 40, 54, 68, 26))
                self.ambientes.append(Ambiente("UH3DORM2", 3, 41, 55, 69, 27))
                self.ambientes.append(Ambiente("UH3DORM3", 3, 42, 56, 70, 28))
                self.ambientes.append(Ambiente("UH3SALA", 2, 43, 57, 71, 29))
		self.ambientes.append(Ambiente("UH4DORM1", 3, 46, 60, 74, 32))
                self.ambientes.append(Ambiente("UH4DORM2", 3, 45, 59, 73, 31))
                self.ambientes.append(Ambiente("UH4DORM3", 3, 44, 58, 72, 30))
                self.ambientes.append(Ambiente("UH4SALA", 2, 47, 61, 75, 33))		
		self.fatal = None
		self.severe = None
		self.warningsCount = 0
		##	PARA ADICIONAR UM AMBIENTE, BASTA ADICIONAR UMA LINHA NO FORMATO ABAIXO, LOGO APOS ELE
		##  @ambientes << Ambiente.new("NOME AMBIENTE", "HEADER DA COLUNA OCUPACAO", "HEADER DA COLUNA RESFRIAMENTO", "HEADER COLUNA AQUECIMENTO", "HEADER COLUNA AQUECIMENTO COMP", "HEADER COLUNA FAN")

	def setMessage(self, _fatal, _severe, _wcount):
		self.fatal=_fatal
		self.severe = _severe
		self.wcount = _wcount

	def pegarAmbientes(self):
		return self.ambientes

	def pegarNome(self):
		return self.casa

	def pegarFatal(self):
		return self.fatal

	def pegarSevere(self):
		return self.severe

	def pegarWarningsCount(self):
		return self.warningsCount

## Classe Ambiente
class Ambiente:
	## ocupacao, resfriamento, aquecimento, aquecimentoComp, FAN)
	def __init__(self, nome, colunaOcupacao, colunaResfriamento, colunaAquecimento, colunaAquecimentoComp, colunaFan):
		self.nome = nome
		self.coluna_ocupacao = colunaOcupacao
		self.coluna_resfriamento= colunaResfriamento
		self.coluna_aquecimento = colunaAquecimento
		self.coluna_aquecimento_comp = colunaAquecimentoComp
		self.coluna_fan = colunaFan
		self.tempo_ocupacao = self.inicializar_somatorio()
		self.consumo_aquecimento = self.inicializar_somatorio()
		self.tempo_uso_aquecimento = self.inicializar_somatorio()
		self.consumo_resfriamento = self.inicializar_somatorio()
		self.tempo_uso_resfriamento = self.inicializar_somatorio()

	def inicializar_somatorio(self):
		somatorios_mensais = {}
		for mes in range(1,13):
			somatorios_mensais[mes] = 0
		return somatorios_mensais

	def pegarNome(self):
		return self.nome


	def somar_linha(self, row):
		mes = self.extrai_mes(row)
		if (float(row[self.coluna_ocupacao]) > 0):
			self.tempo_ocupacao[mes] += float (5)

		if (float(row[self.coluna_aquecimento]) > 0):
			self.consumo_aquecimento[mes] += float(row[self.coluna_aquecimento]) + float(row[self.coluna_aquecimento_comp]) + float(row[self.coluna_fan])
			self.tempo_uso_aquecimento[mes] += float (5)

		if (float(row[self.coluna_resfriamento]) > 0):
			self.consumo_resfriamento[mes] += float(row[self.coluna_resfriamento]) + float(row[self.coluna_fan])
			self.tempo_uso_resfriamento[mes] += float (5)

	def extrai_mes(self, row):
		# 12/31  24:00:00
		str_date = row[0]
		str_date = str_date.strip()
		return int(str_date[:2])


	def get_somatorios_consumos_aquecimento(self):
		lista_consumo_aquecimento = self.get_somatorio_as_list(self.consumo_aquecimento, 3600000)
		return lista_consumo_aquecimento

	def get_somatorios_consumos_resfriamento(self):
		lista_consumo_resfriamento = self.get_somatorio_as_list(self.consumo_resfriamento, 3600000)
		return lista_consumo_resfriamento


	def get_somatorios_consumos(self):
		lista_consumo_aquecimento = self.get_somatorio_as_list(self.consumo_aquecimento, 3600000)
		lista_consumo_resfriamento = self.get_somatorio_as_list(self.consumo_resfriamento, 3600000)
		return lista_consumo_aquecimento + lista_consumo_resfriamento

	def get_somatorios_tempos(self):
		lista_tempo_ocupacao = self.get_somatorio_as_list(self.tempo_ocupacao, 60)
		lista_tempo_uso_aquecimento = self.get_somatorio_as_list(self.tempo_uso_aquecimento, 60)
		lista_tempo_uso_resfriamento = self.get_somatorio_as_list(self.tempo_uso_resfriamento, 60)
		return lista_tempo_ocupacao + lista_tempo_uso_aquecimento + lista_tempo_uso_resfriamento


	def get_somatorio_as_list(self, somatorios_mensais, divisor):
		lista = []

		total = 0
		for mes, somatorio in somatorios_mensais.iteritems():
			somatorio = somatorio / divisor
			lista.append(somatorio)
			total +=  somatorio
		lista.append(total)

		return lista


#------------------------------------------------------------------------------

#def escrever_resultados(nome_caso, ambientes):

#------------------------------------------------------------------------------




def criarCSVResultado(casas):
	enderecoSaidaCSV="";
	#enderecoSaidaCSV='/prj/prjeee/msorgato/casos_temp/resultados/';
	##SE DESEJAR MUDAR O CAMINHO ABSOLUTO AONDE O CSV SERA SALVO, CRIE UMA LINHA NO FORMATO ABAIXO, LOGO APOS ELE
	##enderecoSaidaCSV="/"


	jaExiste = os.path.isfile(enderecoSaidaCSV+"tip5_erros.csv")
	file = open(enderecoSaidaCSV+"tip5_erros.csv", 'a')
	print "Criando relatorio erros"
	wr = csv.writer(file, delimiter=',', quotechar='|')
	if jaExiste==False:
		wr.writerow(["Caso","Warning","Severe","Fatal"])
	for casa in casas:
		ambientes = casa.pegarAmbientes()
		for ambiente in ambientes:
			tudo=[]
			tudo.append(casa.pegarNome())
			tudo.append(casa.pegarWarningsCount())
			tudo.append(casa.pegarSevere())
			tudo.append(casa.pegarFatal())
			wr.writerow(tudo)
	print "CSV Criado"

	jaExiste = os.path.isfile(enderecoSaidaCSV+"tip5_aquecimento.csv")
	file = open(enderecoSaidaCSV+"tip5_aquecimento.csv", 'a')
	print "Criando CSV Aquecimento"
	wr = csv.writer(file, delimiter=',', quotechar='|')
	if jaExiste==False:
		wr.writerow(["Caso","Ambiente","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Anual"])
	for casa in casas:
		ambientes = casa.pegarAmbientes()
		for ambiente in ambientes:
			tudo=[]
			tudo.append(casa.pegarNome())
			tudo.append(ambiente.pegarNome())
			wr.writerow(tudo+ ambiente.get_somatorios_consumos_aquecimento())
	print "CSV Criado"

	jaExiste = os.path.isfile(enderecoSaidaCSV+"tip5_resfriamento.csv")
	file = open(enderecoSaidaCSV+"tip5_resfriamento.csv", 'a')
	print "Criando CSV Resfriamento"
	wr = csv.writer(file, delimiter=',', quotechar='|')
	if jaExiste==False:
		wr.writerow(["Caso","Ambiente","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Anual"])
	for casa in casas:
		ambientes = casa.pegarAmbientes()
		for ambiente in ambientes:
			somatorio = ambiente.get_somatorios_consumos_resfriamento()
			tudo = []
			tudo.append(casa.pegarNome())
			tudo.append(ambiente.pegarNome())
			wr.writerow(tudo + somatorio)
	print "CSV CRIADO"


	jaExiste = os.path.isfile(enderecoSaidaCSV+"tip5_tempo.csv")
	file = open(enderecoSaidaCSV+"tip5_tempo.csv", 'a')
	print "Criando CSV Tempo"
	wr = csv.writer(file, delimiter=',', quotechar='|')
	if jaExiste==False:
		wr.writerow(["Caso","Ambiente","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Anual"])
	for casa in casas:
		ambientes = casa.pegarAmbientes()
		for ambiente in ambientes:
			somatorio = ambiente.get_somatorios_tempos()
			wr.writerow([casa.pegarNome(), ambiente.pegarNome(), ambiente.get_somatorios_tempos()])
	print "CSV CRIADO"


def pegarPastas(diretorio):
	return [name for name in os.listdir(diretorio)
            if os.path.isdir(os.path.join(diretorio, name))]
	teste = []
	for dirname, dirnames,filenames in os.walk(diretorio):
		for dirname in dirnames:
			teste.append(dirname)
	return teste


#------------------------------------------------------------------------------

#------------------------------------------------------------------------------

def processarArquivoCSV(caso):
	print "auiii"
	csvs = find_files(caso, ".csv")
	if (len(csvs)>0):
		casa = Casa(caso)
		print "Processando CSV "+str(casa.pegarNome())
		csvpath =os.path.join(csvs[0])
		csvfile = open(csvpath, "rb")
		csv_file_as_dict = csv.DictReader(csvfile, delimiter=',')
		reader = csv.reader(csvfile)
		reader.next() # skip first line
		ambientes = casa.pegarAmbientes()
		for row in reader:
			for ambiente in ambientes:
				ambiente.somar_linha(row)
		print "CSV Processado"
		shutil.rmtree(caso)
		return casa
	else:
#		print "Nenhum csv encontrado no caso: " + caso
		return None


def process_csv_file(csv_input_file_path):
	fullpath, nome_caso = os.path.split(csv_input_file_path)
	casa = Casa(nome_caso)
	print "processo tipo 2 do CSV "+str(casa.pegarNome())
	csv_input_file = open(csv_input_file_path+'/eplusout.csv')
	csv_reader = csv.reader(csv_input_file, delimiter=',', quotechar='|')

	ambientes = casa.pegarAmbientes ();
	csv_reader.next() # skip first line
	for row in csv_reader:
		for ambiente in ambientes:
			  ambiente.somar_linha(row)
	print "CSV Processado"
	print csv_input_file_path+'/eplusout.err'
	f = open(csv_input_file_path+'/eplusout.err', 'r+b')
	isSevere=False
	isFatal=False
	severe=""
	fatal=""
	wcount = 0
	for line in f:
		if isSevere:
			if "**   ~~~   **" in line:
				severe+="\n"+line
				continue
			else:
				isSevere=False
		if "** Severe  **" in line:
			isSevere = True
			severe+=line
			continue
		if isFatal:
			if "**   ~~~   **" in line:
				fatal+="\n"+line
				continue
			else:
				isFatal=False
		if "** Fatal  **" in line:
			isFatal = True
			fatal+=line
			continue
	#	if ("EnergyPlus Terminated" in line) or ("EnergyPlus Completed Successfully" in line):
	#		i = line.find("Warning;")
	#		i-=2
	#		if (i>0):
	#			j=i
	#			while j.isdigit:
	#				j-=1
	#			wcount=int(line[i:j])
	wcount = 0
	casa.setMessage(fatal, severe, wcount)
	print "deletando "+csv_input_file_path
	#os.system('rm -rf {}'.format(csv_input_file_path))

	shutil.rmtree(csv_input_file_path, ignore_errors=True)
	return casa


#------------------------------------------------------------------------------


#------------------------------------------------------------------------------

def findFolders():
	caminhoAbsolutoPastas=""
	##SE DESEJA ALTERAR O CAMINHO ABSOLUTO DAS PASTAS, CRIE UMA LINHA NO FORMATO ABAIXO, LOGO APOS ELE
	##caminhoAbsolutoPastas="/home/user/"
	csvs = pegarPastas(caminhoAbsolutoPastas+".")
#
	for caso in csvs:
		c = processarArquivoCSV(str(caso))
		if (c):
			casas.append(c)



def find_files(root_path, file_type):
	file_paths = []
	for root, dirs, files in os.walk(root_path):
		for file_name in files:
	  		if file_name.endswith(file_type):
				file_paths.append(os.path.join(root, file_name))
 	return file_paths

#------------------------------------------------------------------------------

def get_csv_file(tar_file_path):
	base_path = os.path.dirname(tar_file_path)
	tmp_dir_path = os.path.join(base_path, 'tmp')

	tar = tarfile.open(tar_file_path)
	tar.extractall(tmp_dir_path)
	tar.close()
	csv_file_path_src = find_files(tmp_dir_path, '.csv')
	if (len(csv_file_path_src)>0):
		csv_file_path_dst = os.path.join(base_path, 'eplusout.csv')
		shutil.move(csv_file_path_src[0], csv_file_path_dst)
		try:
			shutil.rmtree(tmp_dir_path)
		except:
			pass
		return csv_file_path_dst
	else:
		return None

#------------------------------------------------------------------------------

def extract_data(tar_file_path):
	csv_input_file_path = get_csv_file(tar_file_path)
	if not (csv_input_file_path):
		print "NENHUM CSV FOI ENCONTRADO NO ENDERECO: "+tar_file_path
		return None

	print('Processing file: ' + tar_file_path)
	c = process_csv_file(csv_input_file_path)
	if (c):
		casas.append(c);


def start_proccess():
	##EXTRAIR TAR.GZS
	#Procura pelas pastas
	findFolders()
	files = find_files(root_files_path, '.tar.gz')+ find_files(root_files_path, '.tar')
	for file_path in files:
		extract_data(file_path)
	criarCSVResultado(casas)


def start_individual_process(file_path):
	##EXTRAIR TAR.GZS
	#Procura pelas pastas
	casa = []
	c = process_csv_file(file_path)
	if c:
		casa.append(c)
	criarCSVResultado(casa)


#------------------------------------------------------------------------------



root_files_path = os.path.dirname(os.path.realpath(__file__))

if len(sys.argv) != 2:
   print 'use: [program] [input file]'
   exit(1)
restore_path = sys.argv[1]

start_individual_process(restore_path)

#start_proccess()


#print('!!!     PROCESSAMENTO FINALIZADO    !!!')


