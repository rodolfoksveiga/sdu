from __future__ import division
import csv
import os
from pyDOE import *


csv_file_name = 'amostratip1.csv'
idf_file_name = 'tipologia1.idf'
folder_name = 'c'

#### Fatores da amostragem. Para adicionar um novo fator, deve-se adicionar um novo item na variavel "factors"
#factors = ["@@Azimute@@", "@@ParExt@@", "@@Cob@@"] exemplo

_factors = ["@@Pavp@@", "@@Azimute@@", "@@ParExt@@", "@@AbsPar@@", "@@ParInt@@", "@@Cob@@", "@@AbsCob@@", "@@ExpCob@@", "@@PisExt@@", "@@ExpPis@@", "@@Vid@@", "@@FatVen@@", "@@Somb@@"]

#### Parametros dos fatores. Para adicionar uma nova lista de parametros, basta adicionar uma nova linha apos o ultimo fator, seguindo o modelo abaixo
#parameters[indice] = ["parametro 1",...,"parametro n"]

_parameters = {}
_parameters[0] = ["Pavp10.txt", "Pavp15.txt", "Pavp20.txt", "Pavp30.txt"]      # fator 1 - Percentual de area de ventilacao em relacao ao piso
_parameters[1] = ["0", "90", "180", "270"]      # fator 2 - Azimute
_parameters[2] = ["ParExt1", "ParExt2", "ParExt3", "ParExt4", "ParExt5", "ParExt6", "ParExt7", "ParExt8", "ParExt9", "ParExt10", "ParExt11", "ParExt12", "ParExt13", "ParExt14", "ParExt15", "ParExt16", "ParExt17", "ParExt18", "ParExt19", "ParExt20"] # fator 3 - Paredes
_parameters[3] = ["0.3", "0.4", "0.5", "0.6", "0.7", "0.8"]      # fator 7 - Absortancia da parede
_parameters[4] = ["ParInt1", "ParInt2", "ParInt3", "ParInt4", "ParInt5", "ParInt6", "ParInt7"]  # Paredes internas
_parameters[5] = ["Cob1", "Cob2", "Cob3", "Cob4", "Cob5", "Cob6", "Cob7", "Cob8", "Cob9", "Cob10", "Cob11", "Cob12", "Cob13", "Cob14", "Cob15", "Cob16", "Cob17", "Cob18", "Cob19", "Cob20", "Cob21"]  # fator 4 - Coberturas
_parameters[6] = ["0.3", "0.4", "0.5", "0.6", "0.7", "0.8"]      # fator 8 - Absortancia da cobertura
_parameters[7] = ["Outdoors", "Adiabatic"]      # fator 8 - Exposicao da cobertura
_parameters[8] = ["Pis1", "Pis2", "Pis3", "Pis4", "Pis5", "Pis6", "Pis7"]      # fator 5 - Pisos
_parameters[9] = ["OtherSideConditionsModel", "Adiabatic", "Outdoors"]      # fator 5 - Pisos
_parameters[10] = ["Vid1", "Vid2", "Vid3", "Vid4"]      # fator 6 - Vidros
_parameters[11] = ["0.25", "0.50", "0.75", "1.0"]      # fator 6 - Vidros
_parameters[12] = ["SombVeneziana.txt", "SemSomb.txt", "SombBrise60cm.txt", "SombBrise120cm.txt", "SombBrise180cm.txt"]      # fator 9 - Dispositivo de Sombreamento
_samplesSize=7500;

####Transformacao para discreta
def discrete(value, n):
    diff = 1/n
    total=diff
    i=1
    while (total<value):
        i+=1
        total+=diff
    return i


####Gera CSV com as amostras
def generateCSV(factors, lhd, lhd2, csvname, samplesSize):
    with open(csvname, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(factors)
        for i in range(samplesSize):
            wr.writerow(lhd2[i])


#-------------------------------------------------------------------------------------

def create_new_folder(folder_name, folder_number):
    base_path = os.path.dirname(os.path.realpath(__file__))

    folder_number = str(folder_number).zfill(5) #complementa com zeros, 1 => 00001
    current_folder_name = folder_name + folder_number
    directory = os.path.join(base_path, current_folder_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

#-------------------------------------------------------------------------------------

def create_new_idf_file(directory, text, dictionary):
    new_idf_file = open(os.path.join(directory, 'in.idf'), 'w')    
    for key, value in dictionary.items():
        if (os.path.splitext(value)[1]=='.txt'):
            with open(value) as block:
                value = block.read()
                text = text.replace(key, value)
    
    for key, value in dictionary.items():
        if (os.path.splitext(value)[1]!='.txt'):
            text = text.replace(key, value)
    new_idf_file.write(text)

#-------------------------------------------------------------------------------------

def complement_the_dictionary(dictionary):
    if dictionary.get('@@ExpCob@@') == 'Outdoors':
        dictionary['@@ExpCob1@@'] = 'SunExposed'
        dictionary['@@ExpCob2@@'] = 'WindExposed'
    elif dictionary.get('@@ExpCob@@') == 'Adiabatic':
        dictionary['@@ExpCob1@@'] = 'NoSun'
        dictionary['@@ExpCob2@@'] = 'NoWind'

    if dictionary.get('@@ExpPis@@') == 'OtherSideConditionsModel':
        dictionary['@@ExpPis1@@'] = 'GroundCoupledOSCM'
        dictionary['@@ExpPis2@@'] = 'NoWind'
        dictionary['@@ExpPis3@@'] = 'GroundDomain.txt'
    elif dictionary.get('@@ExpPis@@') == 'Adiabatic':
        dictionary['@@ExpPis1@@'] = '   '
        dictionary['@@ExpPis2@@'] = 'NoWind'
        dictionary['@@ExpPis3@@'] = 'Adiabatic.txt'
    elif dictionary.get('@@ExpPis@@') == 'Outdoors':
        dictionary['@@ExpPis1@@'] = '   '
        dictionary['@@ExpPis2@@'] = 'WindExposed'
        dictionary['@@ExpPis3@@'] = 'Outdoors.txt'

    if dictionary.get('@@Somb@@') == 'SombVeneziana.txt':
        dictionary['@@Somb1@@'] = 'Somb'
        dictionary['@@Somb2@@'] = '    '
    elif dictionary.get('@@Somb@@') == 'SemSomb.txt':
         dictionary['@@Somb1@@'] = '    '
         dictionary['@@Somb2@@'] = '    '
    elif ((dictionary.get('@@Somb@@') == 'SombBrise60cm.txt') and (dictionary.get('@@Pavp@@') == 'Pavp10.txt')):
         dictionary['@@Somb1@@'] = '    '
         dictionary['@@Somb2@@'] = 'brise60cm10.txt'
    elif ((dictionary.get('@@Somb@@') == 'SombBrise120cm.txt') and (dictionary.get('@@Pavp@@') == 'Pavp10.txt')):
         dictionary['@@Somb1@@'] = '    '
         dictionary['@@Somb2@@'] = 'brise120cm10.txt'
    elif ((dictionary.get('@@Somb@@') == 'SombBrise180cm.txt') and (dictionary.get('@@Pavp@@') == 'Pavp10.txt')):
         dictionary['@@Somb1@@'] = '    '
         dictionary['@@Somb2@@'] = 'brise180cm10.txt'
    elif ((dictionary.get('@@Somb@@') == 'SombBrise60cm.txt') and (dictionary.get('@@Pavp@@') == 'Pavp15.txt')):
         dictionary['@@Somb1@@'] = '    '
         dictionary['@@Somb2@@'] = 'brise60cm15.txt'
    elif ((dictionary.get('@@Somb@@') == 'SombBrise120cm.txt') and (dictionary.get('@@Pavp@@') == 'Pavp15.txt')):
         dictionary['@@Somb1@@'] = '    '
         dictionary['@@Somb2@@'] = 'brise120cm15.txt'
    elif ((dictionary.get('@@Somb@@') == 'SombBrise180cm.txt') and (dictionary.get('@@Pavp@@') == 'Pavp15.txt')):
         dictionary['@@Somb1@@'] = '    '
         dictionary['@@Somb2@@'] = 'brise180cm15.txt'
    elif ((dictionary.get('@@Somb@@') == 'SombBrise60cm.txt') and (dictionary.get('@@Pavp@@') == 'Pavp20.txt')):
         dictionary['@@Somb1@@'] = '    '
         dictionary['@@Somb2@@'] = 'brise60cm20.txt'
    elif ((dictionary.get('@@Somb@@') == 'SombBrise120cm.txt') and (dictionary.get('@@Pavp@@') == 'Pavp20.txt')):
         dictionary['@@Somb1@@'] = '    '
         dictionary['@@Somb2@@'] = 'brise120cm20.txt'
    elif ((dictionary.get('@@Somb@@') == 'SombBrise180cm.txt') and (dictionary.get('@@Pavp@@') == 'Pavp20.txt')):
         dictionary['@@Somb1@@'] = '    '
         dictionary['@@Somb2@@'] = 'brise180cm20.txt'
    elif ((dictionary.get('@@Somb@@') == 'SombBrise60cm.txt') and (dictionary.get('@@Pavp@@') == 'Pavp30.txt')):
         dictionary['@@Somb1@@'] = '    '
         dictionary['@@Somb2@@'] = 'brise60cm30.txt'
    elif ((dictionary.get('@@Somb@@') == 'SombBrise120cm.txt') and (dictionary.get('@@Pavp@@') == 'Pavp30.txt')):
         dictionary['@@Somb1@@'] = '    '
         dictionary['@@Somb2@@'] = 'brise120cm30.txt'
    elif ((dictionary.get('@@Somb@@') == 'SombBrise180cm.txt') and (dictionary.get('@@Pavp@@') == 'Pavp30.txt')):
         dictionary['@@Somb1@@'] = '    '
         dictionary['@@Somb2@@'] = 'brise180cm30.txt'

#-------------------------------------------------------------------------------------

def start(csv_file_name, idf_file_name, folder_name, factors, parameters, samplesSize):
    idf_file = open(idf_file_name)
    idf_file_text = idf_file.read()
    idf_file.close()



    lhd = lhs(len(parameters), samples=samplesSize)
    lhd2 = []
    for i in range(samplesSize):
        row = []
        for j in range(len(parameters)):
            row.append(str(parameters[j][int(discrete(lhd[i][j],len(parameters[j])))-1]))
        lhd2.append(row)
    generateCSV(factors, lhd, lhd2, csv_file_name, samplesSize)


    csvfile = open(csv_file_name)
    csv_file_as_dict = csv.DictReader(csvfile, delimiter=',')

    folder_number = 0
    for dictionary in csv_file_as_dict:
        complement_the_dictionary(dictionary)

        directory = create_new_folder(folder_name, folder_number)

        create_new_idf_file(directory, idf_file_text, dictionary)

        # NEXT FOLDER
        folder_number = folder_number + 1
        
    csvfile.close()
    idf_file.close()

#-------------------------------------------------------------------------------------

start(csv_file_name, idf_file_name, folder_name, _factors, _parameters, _samplesSize)
