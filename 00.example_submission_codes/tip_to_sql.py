import sqlite3
import os
import csv
import subprocess
import time

def take_paths():
	paths = []
	for directories in os.listdir(absolute_path):
		if not (os.path.isfile(directories)):
			paths.append(os.path.join(absolute_path, directories))

	paths.sort()
	return paths

def path_to_saida():
	path_to_saida = []
	index_tip = 1
	paths = take_paths()

	for path in paths:
		if (os.path.isfile(path + "/saida_tip" + str(index_tip) + ".csv")):
			path_to_saida.append(path + "/saida_tip" + str(index_tip) + ".csv")

		index_tip += 1
	return path_to_saida


def string_to_file(string):
	file = open(string, 'rU+')
	return file

def fix_csv():
	paths = take_paths()
	global tip
	tip = 1

	paths.pop(0)
	paths.pop(0)
	for element in paths:
		in_file = string_to_file(element + "/resultados/tip" + str(tip) + "_tempo.csv")
		out_file = open("tip"+str(tip)+"/resultados/tip" + str(tip) + "_tempo_repaired.csv", 'w+')

		csv_reader = csv.reader(in_file, delimiter = ',')
		csv_writer = csv.writer(out_file, delimiter = ',')
		conversion = set('|[]|')

		for row in csv_reader:
			newrow = [''.join('' if c in conversion else c for c in entry) for entry in row]
			csv_writer.writerow(newrow)
		tip += 1



def config_csv():
	fix_csv()
	paths = take_paths()
	global tip
	tip = 1

	paths.pop(0)
	paths.pop(0)
	for path in paths:
		file = string_to_file(path + "/resultados/tip" + str(tip) + "_tempo_repaired.csv")
		out_file = open("tip"+str(tip)+"/resultados/tip" + str(tip) + "_tempo_repaired_final.csv", 'w+')
		file.seek(0)
		csv_writer = csv.writer(out_file, delimiter=',', quotechar='|')
		csv_writer.writerow(["Caso", "Ambiente", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul","Aug", "Sep", "Oct", "Nov", "Dec", "Anual","Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul","Aug", "Sep", "Oct", "Nov", "Dec", "Anual","Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul","Aug", "Sep", "Oct", "Nov", "Dec", "Anual", "Hdesconf", "Phoras"])
		csv_reader = csv.reader(file, delimiter=',', quotechar='|')
		csv_reader.next()

		for row in csv_reader:
			row_aux = [float(row[27])+float(row[40]), (float(row[14])-float(row[27])-float(row[40]))/float(row[14])]
			newrow = row + row_aux
			csv_writer.writerow(newrow)
		tip += 1

def csv_to_sql_erros(cursor, csv_file):
	csv_reader = csv.reader(csv_file, delimiter = ',', quotechar = '|')
	csv_reader.next()

	for row in csv_reader:
		insert = """INSERT INTO Erros
		            VALUES (DEFAULT, %s, %s, %s, %s) """
		cursor.execute(insert, (row[0], row[1], row[2], row[3]))


def csv_to_sql_others(csv_file, case):
	conn = sqlite3.connect('../resultado_analise.db')
	cursor = conn.cursor()

	csv_file.seek(0)
	csv_reader = csv.reader(csv_file, delimiter = ',', quotechar = '|')
	csv_reader.next()

	if case == 1:
		for row in csv_reader:
			insert = """INSERT INTO Aquecimento
						VALUES ('%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
			insert = insert % (city_name, tip, row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14])
			cursor.execute(insert)

	elif case == 2:
		for row in csv_reader:
			insert = """INSERT INTO Resfriamento
						VALUES ('%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
			insert = insert % (city_name, tip, row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14])
			cursor.execute(insert)

	elif case == 3:
		for row in csv_reader:
			insert = """INSERT INTO Tempo
						VALUES ('%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

			insert = insert % (city_name, tip, row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14], row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35],row[36],row[37],row[38],row[39],row[40],row[41],row[42])
			cursor.execute(insert)

	elif case == 4:
		for row in csv_reader:
			insert = """INSERT INTO Erros
						VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"""

			insert = insert % (city_name, tip, row[0], row[1], row[2], row[3])
			cursor.execute(insert)

	conn.commit()
	cursor.close()

def insert_into():
	global tip
	tip = 1
	paths = take_paths()
	paths.pop(0)
	paths.pop(0)
	for element in paths:
		path = element + "/resultados/"
		my_file = string_to_file(path + "tip" + str(tip) + "_aquecimento.csv")
		csv_to_sql_others(my_file, 1)

		my_file = string_to_file(path + "tip" + str(tip) + "_resfriamento.csv")
		csv_to_sql_others(my_file, 2)

		my_file = string_to_file(path + "tip" + str(tip) + "_tempo_repaired_final.csv")
		csv_to_sql_others(my_file, 3)

		# my_file = string_to_file(path + "tip" + str(tip) + "_erros.csv")
		# csv_to_sql_others(my_file, 4)
		tip += 1


tip = 1
absolute_path = os.getcwd()
city_name = os.path.basename(os.path.normpath(absolute_path))
config_csv()
insert_into()

