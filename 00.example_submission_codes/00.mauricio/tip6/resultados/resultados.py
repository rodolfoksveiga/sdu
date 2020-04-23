import os
import csv
import shutil
import sys
import codecs
from math import sqrt

##
## @brief      This function is not of my authorship. I taken from:
##             http://codeselfstudy.com/blogs/how-to-calculate-standard-deviation-in-python.
##             It calculates a standard deviation from a list of numbers.
##
## @param      lst         The list containing the numbers.
## @param      population  No idea what this means.
##
## @return     Return the value that represents the standard deviation of the
##             informed list.
##
def standardDeviation(lst, population=True):
	num_items = len(lst)
	mean = sum(lst) / num_items
	differences = [x - mean for x in lst]
	sq_differences = [d ** 2 for d in differences]
	ssd = sum(sq_differences)

	# Note: it would be better to return a value and then print it outside
	# the function, but this is just a quick way to print out the values along
	# the way.
	if population:
		variance = ssd / num_items
	else:
		variance = ssd / (num_items - 1)
	sd = sqrt(variance)
	return sd

##
## @brief      Reads the city and the state that was simulated. It just open
##             the epw file, reads the first line as a list. At last, closes
##             the file, removes the epw file and return the necessary data.
##
## @param      case  The case that had been simulated.
##
## @return     Return a tuple where the first element is the city and the
##             second is the state.
##
def readCityState(case):
	with codecs.open(case + 'in.epw', 'r', encoding='iso-8859-1') as f:
		firstLine = f.readline()
		row = [column.strip() for column in firstLine.split(',')]

		f.close()

##	os.remove(case + 'in.epw')
	return row[1], row[2]

##
## @brief      This function opens the 'inTable.csv' file in the current
##             directory with the csv reader. It iterates through each row
##             until finds the string 'Net Conditioned Building Area' in the
##             second column. When founds, it closes the file and return
##             the area of the building that is at the the third column.
##
## @param      case  The case that had been simulated
##
## @return     Return the area of the building.
##
def readArea(case):
	with codecs.open(case + 'eplustbl.csv', 'r', encoding='iso-8859-1') as f:
		csvReader = csv.reader(f, delimiter=',')
		for row in csvReader:
			if len(row) >= 2 and row[1] == 'Net Conditioned Building Area':
				f.close()
				return float(row[2])
			
def readHoras(case):
	with codecs.open(case + 'eplustbl.csv', 'r', encoding='iso-8859-1') as f:
		csvReader = csv.reader(f, delimiter=',')
		for row in csvReader:
			if len(row) >= 2 and row[1] == 'Time Setpoint Not Met During Occupied Cooling':
				f.close()
				return float(row[2])


##
## @brief      This functions open the 'inTable.csv' in at the current directory
##             as a csv reader. After that, it iterate through each that has a
##             content until find the string 'Electricity [kWh]'. Reach this
##             string, meanig that the we are next to the aimed values. For
##             next rows, we check the second column. If they have 'Cooling',
##             'Fans', 'Pumbs', 'Heat Rejection' or 'Total End Uses' values,
##             then we put this values and the respective consume values in
##             our dictionary (i.e. hash table). After read the 'Total End Uses'
##             variable, breaks the loop, close the file and return the hash.
##
## @param      case  The case that had been simulated
##
## @return     Returns a ha
##sh table that map the strings 'Cooling', 'Fans',
##             'Pumps', 'Heat Rejection' and 'Total End Uses' to the respective
##             values of electricity consume.
##
def readConsume(case):
	findElectricity = False
	consume = []
	csvFile = open(case + 'eplustbl.csv', 'r', encoding='iso-8859-1')
	csvReader = csv.reader(csvFile, delimiter=',')

	for row in csvReader:
		if len(row) >= 3 and row[2] == 'Electricity [kWh]':
			findElectricity = True
		else:
			if findElectricity and len(row) >= 3:
				if row[1] == 'Cooling':
					consume.append(row[2])
				elif row[1] == 'Fans':
					consume.append(row[2])
				elif row[1] == 'Pumps':
					consume.append(row[2])
				elif row[1] == 'Heat Rejection':
					consume.append(row[2])
				elif row[1] == 'Total End Uses':
					break

	csvFile.close()
	return consume

##
## @brief      This function iterates for each memmber in our hash table
##             'consume'. For each entry on the hash, takes the respective value
##             and append into a list divided by the area. Also, it sums the
##             respective value into accumulator. Repeat the process for each
##             entry and, at the end, appends the accumulator into the list.
##
## @param      consume  The consume of electricity divide by type of
##                      equipment. Taken from the 'readConsume' function. See
##                      its documentation for more info.
## @param      area     The area of the building, taken from the 'readArea'
##                      function. See its documentation for more info.
##
## @return     A list containing the consume by square meter of each type
##             of electricity equipment.
##
def calculateConsumeBySquareMeter(consume, area):
	total = 0.0
	consumeBySquareMeter = []

	for c in consume:
		aux = float(c)
		total += aux/area
		consumeBySquareMeter.append(aux/area)

	consumeBySquareMeter.append(total)
	return consumeBySquareMeter

##
## @brief      This function open the 'inTable.csv' file at the current
##             current directory as csv reader. Then, will iterate through
##             each row until find the string 'Equipment Summary'. When meet
##             this string, we now that the next lines will may have our
##             chiller values that we want (the chiller values can vary from
##             1 to 4). Other important comment, the string 'CHILLER' can
##             also appear at the end of the of the csv, so if the follow
##             sequence of 'CHILLER' is broke, we know that we get all possible
##             values of the chillers. Finally, we just append the values
##             into a list, close and remove the file and return the list.
##
## @param      case  The case that had been simulated
##
## @return     Get a list of lenght upon to 4 values from the chiller values
##             in the csv. The number of chillers depend of the simulation.
##
def getChillerValues(case):
	findEquipment = False
	chillers = 0
	chillerValues = []
	csvFile = open(case + 'eplustbl.csv', 'r', encoding='iso-8859-1')
	csvReader = csv.reader(csvFile, delimiter=',')

	for row in csvReader:
		if not findEquipment:
			if len(row) >= 2 and row[1] == 'Equipment Summary':
				findEquipment = True
			newRow = row
		else:
			newRow = row
			if len(row) >= 4 and 'CHILLER' in row[1] and chillers < 4:
				chillerValues.append(newRow[3])
				chillers += 1
			elif len(row) >= 2 and 'CHILLER' not in row[1] and chillers > 0:
				break

	csvFile.close()
##	os.remove(case + 'eplustbl.csv')
	return chillerValues

##
## @brief      This function just transform the chiller values from Wats to
##             Tons.
##
## @param      chillerValues  The chiller values obtained from the
##             'getChillerValues' function. See its documentation for more info.
##
## @return     A list containing the chiller values in Tons.
##
def chillerValuesToTons(chillerValues):
	chillerValues = [float(c) * 2.843451 * 10**-4 for c in chillerValues]
	return chillerValues

##
## @brief      This function open the 'in.csv' file in the current directory
##             using the csv reader. If not found the column of the enthalpies
##             yet, then will iterate using a index through each column until
##             find the enthalpies column. After find it, it will append all
##             enthalpy values into a list. Finally, closes the file and
##             return the list
##
## @param      case  The case that had been simulated
##
## @return     Return all the enthalpy values in the 'Air Enthalpy' column
##             of the 'in.csv' file.
##
def readEnthalpies(case, onlyPartial):
	i = 0
	foundEnthalpy = False
	enthalpies = []
	csvFile = open(case + 'eplusout.csv', 'r', encoding='iso-8859-1')
	csvReader = csv.reader(csvFile, delimiter=',')

	for row in csvReader:
		if foundEnthalpy:
			if onlyPartial and int(float(row[20])) == 1:
				enthalpies.append(row[i])
			elif not onlyPartial:
				enthalpies.append(row[i])
		else:
			for element in row:
				if not 'Environment:Site Outdoor Air Enthalpy' in element:
					i += 1
				else:
					foundEnthalpy = True
					break

	csvFile.close()
	return enthalpies

def readTemperatures(case, onlyPartial):
	i = 0
	foundTemperature = False
	temperatures = []
	csvFile = open(case + 'eplusout.csv', 'r', encoding='iso-8859-1')
	csvReader = csv.reader(csvFile, delimiter=',')

	for row in csvReader:
		if foundTemperature:
			if onlyPartial and int(float(row[20])) == 1:
				temperatures.append(row[i])
			elif not onlyPartial:
				temperatures.append(row[i])
		else:
			for element in row:
				if not 'Environment:Site Outdoor Air Drybulb Temperature' in element:
					i += 1
				else:
					foundTemperature = True
					break

	csvFile.close()
	return temperatures




##
## @brief      This functions open the 'in.csv' file with a csv reader. Also,
##             this function creates a temporary csv file called 'chillers.csv'
##             just to store temporarily the read values. It iterates through
##             each row. If it's the first iteration, iterate through each
##             column until find the columns that have the string
##             'Chiller Evaporator Cooling Energy'. For all this columns, will
##             apend the respective index into a list. After iterate through
##             each column, goes back to the normal loop. For each index
##             in our indexes list, will write the csv values into our
##             temporary csv. The process is repeated for all rows. At the
##             end just remove the close all files and remove the 'in.csv' file.
##
## @param      case  The case that had been simulated
##
## @return     This is a void function
##
def writeChillers(case):
	firstTime = True
	i = 0
	indexes = []
	newRow = []
	csvFile = open(case + 'eplusout.csv', 'r', encoding='iso-8859-1')
	csvChillers = open(case + 'chillers.csv', 'w', encoding='iso-8859-1')
	csvReader = csv.reader(csvFile, delimiter=',')
	csvWriter = csv.writer(csvChillers, delimiter=',')

	for row in csvReader:
		if not firstTime:
			for index in indexes:
				if int(float(row[20])) == 1:
					newRow.append(row[index])
			if newRow:
				csvWriter.writerow(newRow)
			newRow = []
		else:
			for column in row:
				if 'Chiller Evaporator Cooling Energy' in column:
					indexes.append(i)

				i += 1
			firstTime = False

	csvChillers.close()
	csvFile.close()
##	os.remove(case + 'eplusout.csv')

##
## @brief      This function read the values from the 'chillers.csv' file
##             (OBS: this file is created at the 'writeChillers' function
##             see its doc for more info). For each row and for each column of
##             each row, uses an accumulator variable. Then, just convert the
##             accumulator to Jaule and divide by the area in m². Finally,
##             append the value into a list and reset the accumulator. At
##             the end, closes the file and remove it.
##
## @param      case  The case that had been simulated
## @param      area  The area of the building. Obtained from the function
##             'readArea'. See its doc for more info.
##
## @return     The chiller values already ajusted to J/m².
##
def chillerFromJouleToKW(case, area):
	writeChillers(case)
	total = 0.0
	newChillerValues = []
	csvFile = open(case + 'chillers.csv', 'r', encoding='iso-8859-1')
	csvReader = csv.reader(csvFile, delimiter=',')

	for row in csvReader:
		for column in row:
			total += float(column)

		total *= 2.7778*10**-7
		newChillerValues.append(total/area)
		total = 0.0

	csvFile.close()
##	os.remove(case + 'chillers.csv')
	return newChillerValues

##
## @brief      This function iterate through each value in the
##             'newChillerValues' and for each value calculates its percentage
##             multiplying by 100 and dividing by the greatest value on the
##             list. After that, just append the value into a list. Return
##             the list at the end.
##
## @param      newChillerValues  The chiller values in J/m². Obtained from the
##                               function 'chillerFromJouleToKW'. See its
##                               doc for more info.
## @param      maxChiller        The greatest value from the list
##                               'newChillerValues'.
##
## @return     The chiller values calculated in percentage.
##
def calculateChillerPercentage(newChillerValues, maxChiller):
	chillerPecentage = []

	for chiller in newChillerValues:
		result = (float(chiller) * 100) / maxChiller
		chillerPecentage.append(result)

	return chillerPecentage

##
## @brief      This function creates a list which size is 20, since we want
##             that our histogram be divided into 20 segments. Each position
##             is filled with 0's so we can count how many occurances had been.
##             The objective is to divide our interval in 5 to 5. So we
##             calculate if the percentage of the chiller is in 0 ~ 5, 5 ~ 10,
##             and so go on until 95 ~ 100. In this division of intervals, the
##             lower bound is not attended, while the upper bound is.
##
## @param      chillerPercentage  The chiller percentage obtained from the
##             'calculateChillerPercentage' function. See its documentation for
##             more info.
##
## @return     A list containing all the occurances at the interval of 0 ~ 100
##             divided into 20 intervals of 5
def calculateHistogram(chillerPercentage):
	i = 0
	histogram = []
	while i < 20:
		histogram.append(0)
		i += 1

	for percentage in chillerPercentage:
		mod = int(percentage/5)
		if int(mod) == 20:
			index = int(mod) - 1
		else:
			index = int(mod)
		histogram[index] += 1

	histogram = [(hist*100)/len(chillerPercentage) for hist in histogram]
	return histogram

##
## @brief      Calculates the hm using some engineer logic.
##
## @param      enthalpies  The enthalpies obtained from the function
##                         'readEnthalpies'.
##
## @return     The enthalpies after passing by a filter
##
def calculateHM(enthalpies):
	newEnthalpies = [float(enthalpy)/1000 for enthalpy in enthalpies]
	hm = [enthalpy - 35 for enthalpy in newEnthalpies]
	hm = [h for h in hm if h > 0]
	hm = [h + 35 for h in hm]

	return hm

##
## @brief      Calculates the h maximum.
##
## @param      enthalpies  The enthalpies obtained from the function
##                         'readEnthalpies'.
##
## @return     The minimun of the max of the enthalpies
##
def calculateHMax(enthalpies):
	hMax_aux = 200
	hMax = 200
	enthalpies = [float(enthalpy)/1000 for enthalpy in enthalpies]

	for enthalpy1 in enthalpies:
		x = 0
		for enthalpy2 in enthalpies:
			if enthalpy2 > enthalpy1:
				x += 1

		pp = x/len(enthalpies)
		if pp <= 0.004:
			hMax_aux = float(enthalpy1)

		if hMax_aux < hMax:
			hMax = hMax_aux

	return hMax

##
## @brief      Calculates the standar deviation. See 'calculateHM' and
##             'standarDeviation' documentation for more info.
##
## @param      enthalpies  The enthalpies obtained from the function
##                         'readEnthalpies'.
##
## @return     The standar deviation using the hm.
##
def calculateSD(enthalpies):
	hm = calculateHM(enthalpies)
	sdHM = standardDeviation(hm)
	return sdHM

##
## @brief      Don't ask. Jusc accept it and cry.
##
## @param      enthalpies  The enthalpies obtained from the function
##                         'readEnthalpies'. See its doc for more info.
##
## @return     The new enthalpy values.
##
def calculateChe(enthalpies, hMax, temperatures):
	enthalpies = [float(enthalpy)/1000 for enthalpy in enthalpies]
	hm = [enthalpy - 35 for enthalpy in enthalpies]
	for i in range(len(enthalpies)):
		if float(temperatures[i]) < 18:
			hm[i]=0

	hm = [h for h in hm if h > 0]
	sumHM = sum(hm)

	che = sumHM/(hMax - 48)
	return che

##
## @brief      This function checks if the 'resultados.csv' file exists. If
##             not, it will create a header for the csv and wrote. At the end
##             just close the file. Not much more to say about it.
##
## @return     This is a void function.
##
def testFileAndWriteHeader():
	if not os.path.isfile('resultados.csv'):
		i = 0
		header = ['Case', 'City', 'State', 'Area', 'Horas nao atendidas']
		header += ['Cooling consume by m²', 'Fans by m²']
		header += ['Pumps consume by m²', 'Heat rejection consume by m²', 'Total consumption']
		header += ['Nominal Capacity C1', 'Nominal Capacity C2']
		header += ['Nominal Capacity C3', 'Nominal Capacity C4']
		header += ['Maximum demand', 'Anual demand', 'Hmax', 'Che Total']
		header += ['Che Parcial', 'Desvio Total', 'Desvio Parcial']
		while i < 20:
			header.append('H' + str(i))
			i += 1

		csvOut = open('resultados.csv', 'a', encoding='iso-8859-1')
		csvWriter = csv.writer(csvOut, delimiter=',')
		csvWriter.writerow(header)
		csvOut.close()

##
## @brief      This function is responsible for test if the 'resultados.csv'
##             exists or not and wrote the header in the csv file if not exists.
##             Finally, it just wrote the row using the csv writer and closes
##             the file.
##
## @param      row   The row that will be wrote in the 'resultados.csv' file
##
## @return     This is a void function.
##
def writeFinalValues(row):
	testFileAndWriteHeader()
	csvOut = open('resultados.csv', 'a', encoding='iso-8859-1')
	csvWriter = csv.writer(csvOut, delimiter=',')
	csvWriter.writerow(row)
	csvOut.close()

##
## @brief      This funciton tries to remove the folder of the case. If not be
##             able to do that, this means that the directory still having some
##             content and the an error occured during the simulation. For that
##             we will just print a message of error.
##
## @param      case  The case that had been simulated
##
## @return     This is a void function
##
def deleteCase(case):
	try:
		shutil.rmtree(case, ignore_errors=True)
	except Exception as e:
		print('Não foi possível deletar a pasta do caso: ' + case)

##
## @brief      This is the 'main' of the script. It makes all necessary changes
##             in the csv files and write all the data on the 'resultados.csv'
##             file at the current directory.
##
## @param      case  The case (path) that had been simulated
##
## @return     This is a void function
##
def run(case):
	## Read the city and the state from the EPW
	cityState = readCityState(case)
	## Read the area from the 'inTabe.csv'
	area = readArea(case)
	horas = readHoras(case)
	## Read the consume of the equipments from the 'inTable.csv'
	consume = readConsume(case)
	## Calculate the consume of each equipment by m²
	consumeBySquareMeter = calculateConsumeBySquareMeter(consume, area)

	## Get the chiller values from the 'inTable.csv' file
	chillerValues = getChillerValues(case)
	## Transform the chiller values from W to TR
	chillerValuesTons = chillerValuesToTons(chillerValues)
	while len(chillerValuesTons) < 4:
		chillerValuesTons.append('')

	## Read the value of the enthalpies at the 'in.csv' file
	totalEnthalpies = readEnthalpies(case, False)
	partialEnthalpies = readEnthalpies(case, True)
	totalTemperatures = readTemperatures(case, False)
##	print(totalEnthalpies)
	## Calculates the hMax and the che, standard deviation for the total and
	## partial values of enthalpies
	hMax = calculateHMax(totalEnthalpies)
	cheTotal = calculateChe(totalEnthalpies, hMax, totalTemperatures)
	chePartial = calculateChe(partialEnthalpies, hMax, totalTemperatures)
	sdTotal = calculateSD(totalEnthalpies)
	sdPartial = calculateSD(partialEnthalpies)

	## Get the chiller values from the temporary file 'chillers.csv' and
	## transform from joule to Kwh
	chillerValues = chillerFromJouleToKW(case, area)

	## Get the max value of the list 'chillerValues'
	maxChiller = max(chillerValues)
	## Calculates the sum of the list 'chillerValues'
	totalChiller = sum(chillerValues)

	## Calculates the percentage of each chiller
	chillerPercentage = calculateChillerPercentage(chillerValues, maxChiller)
	## Calculates a histogram of 20 intervals for the chiller percentage.
	histogram = calculateHistogram(chillerPercentage)

	## Creates the row that will be written in the csv.
	row = [os.path.basename(os.path.normpath(case))]
	row += list(cityState) + [area] + [horas] + consumeBySquareMeter + chillerValuesTons
	row += [maxChiller, totalChiller, hMax, cheTotal, chePartial, sdTotal]
	row += [sdPartial] + histogram
	## Writes the row in the 'resultado.csv' file.
	writeFinalValues(row)
	## Delete the directory of the case that has been simulated.
	deleteCase(case)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('Use: python resultados.py [input directory]')
		exit(1)

	case = list(sys.argv)[1]
	if not case.endswith('/'):
		case += '/'

	run(case)
