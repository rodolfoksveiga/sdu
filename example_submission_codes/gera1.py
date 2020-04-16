from __future__ import division
import csv
import os
from pyDOE import *


csv_file_name = 'amostra1.csv'
idf_file_name = 'esqueleto.idf'
epw_file_name = 'esqueleto.epw'
folder_name = 'caso'

#### Fatores da amostragem. Para adicionar um novo fator, deve-se adicionar um novo item na variavel "factors"

_factors = ["@@tipo_vent@@", "@@pressao_vent@@", "@@eco_recup@@", "@@c_not@@", "@@renova@@", "@@pressao_bomba_ag@@", "@@pressao_bomba_cond@@", "@@t_bombas@@", "@@r_ag@@", "@@chil@@", "@@inf@@", "@@dpi@@", "@@os@@", "@@apar@@", "@@acob@@", "@@fs@@", "@@uvidro@@", "@@upar@@", "@@ctpar@@", "@@ucob@@", "@@ctcob@@", "@@ctint@@", "@@temp@@", "@@pavtos@@", "@@p@@", "@@rel@@", "@@wwr@@", "@@horas@@", "@@ocup@@", "@@clima@@", "@@nch@@"]

#### Parametros dos fatores. Para adicionar uma nova lista de parametros, basta adicionar uma nova linha apos o ultimo fator, seguindo o modelo abaixo
#parameters[indice] = ["parametro 1",...,"parametro n"]

_parameters = {}
_parameters[0] = ["0", "1"]      # Tipo de ventilacao 0-VAC ou 1-VAV
_parameters[1] = ["150", "250", "350", "450", "550", "650", "750"]      # Pressao do ventilador
_parameters[2] = ["0", "1", "2"] # Uso de ciclo economizador/recuperador de calor 0-"OnOff", 1-"OffOn", 2-"OffOff"
_parameters[3] = ["0"]      # Uso de ciclo noturno 0-off ou 1-on
_parameters[4] = ["0", "1", "2"]  # nivel de renovacao de ar 0-Nivel 1, 1-Nivel 2 ou 2-Nivel 3
_parameters[5] = ["250000", "350000", "450000", "550000", "650000", "750000", "850000"]  # Pressao total das bombas de agua gelada
_parameters[6] = ["100000", "200000", "300000", "400000", "500000", "600000"]  # Pressao da bomba de agua de condensacao
_parameters[7] = ["0", "1", "2"] # Tipo de bombeamento de agua gelada 0-ConstantPrimaryVariableSecondary, 1-ConstantPrimaryNoSecondary, 2-VariablePrimaryNoSecondary
_parameters[8] = ["0"]  # Uso de reset de agua gelada -0-off ou 1 - on
_parameters[9] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]  # Chillers
_parameters[10] = ["0.0", "0.25", "0.5", "0.75"] # infiltracao ACH
_parameters[11] = ["7.5", "10.0", "12.5", "15.0"] # densidade de potencia iluminacao W/m2
_parameters[12] = ["0", "45", "90", "135"] # orientacao solar
_parameters[13] = ["0.4"] # absortancia da parede externa
_parameters[14] = ["0.5"] # absortancia da cobertura
_parameters[15] = ["0.2", "0.35", "0.5", "0.65", "0.8"] # fator solar do vidro
_parameters[16] = ["5.8", "2.7", "1.7"] # transmitancia do vidro
_parameters[17] = ["2.6"] # transmitancia da parede externa
_parameters[18] = ["145"] # capacidade termica da parede externa
_parameters[19] = ["1.93"] # transmitancia da cobertura
_parameters[20] = ["106"] # capacidade termica da cobertura
_parameters[21] = ["145"] # capacidade termica das paredes internas
_parameters[22] = ["20", "22", "24"] # temperatura do termostato para resfriamento
_parameters[23] = ["5", "10", "30", "50"] # numero de pavtos
_parameters[24] = ["10", "15", "30", "50"] # menor dimensao da edificacao
_parameters[25] = ["1", "2.5", "4", "5.5"] # relacao de aspecto entre dimensoes da base
_parameters[26] = ["0.15", "0.35", "0.55", "0.75", "0.95"] # wwr
_parameters[27] = ["8", "10", "12", "14", "16"] # numero de horas de funcionamento em dias de semana
_parameters[28] = ["3.0", "7.0", "11.0", "15.0"] # indice de ocupacao em m2/pessoa
_parameters[29] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"] #zona climatica
_parameters[30] = ["1", "2", "3", "4"] #numero de chillers
_samplesSize=25000;

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

    folder_number = str(folder_number).zfill(6) #complementa com zeros, 1 => 00001
    current_folder_name = folder_name + folder_number
    directory = os.path.join(base_path, current_folder_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

#--------------------------------------------------------------------------------------

def create_new_epw_file(directory, text, dictionary):
    new_epw_file = open(os.path.join(directory, 'in.epw'), 'w')    
    for key, value in dictionary.items():
        if (os.path.splitext(value)[1]=='.txt'):
            with open(value) as block:
                value = block.read()
                text = text.replace(key, value)
    
    for key, value in dictionary.items():
        if (os.path.splitext(value)[1]!='.txt'):
            text = text.replace(key, value)
    new_epw_file.write(text)
    
#-------------------------------------------------------------------------------------
   
def create_new_idf_file(directory, text, dictionary):
    new_idf_file = open(os.path.join(directory, 'in0.idf'), 'w')    
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
#
    p=float(dictionary.get('@@p@@'))
    rel=float(dictionary.get('@@rel@@'))
    wwr=float(dictionary.get('@@wwr@@'))
    pavtos=float(dictionary.get('@@pavtos@@'))
    l=p*rel
    ap=4.5
    zm=3*int(pavtos/2)
    za=3*(pavtos-1)
    lap=l-ap
    apn=(-1)*ap
    pap=p-ap
    ln=(-1)*l
    lapn=(-1)*lap
    pn=(-1)*p
    papn=(-1)*pap
    lapap=l-2*ap
    apap=p-2*ap
#
    hw=3*(wwr**0.5)
    rww=l/3
    lww=rww*hw
    xx=(l-lww)/2
    zw=(3-hw)/2
    rw=p/3
    lw=rw*hw
    x=(p-lw)/2
    dictionary['@@l@@'] = str(l)
    dictionary['@@ap@@'] = str(ap)
    dictionary['@@zm@@'] = str(zm)
    dictionary['@@za@@'] = str(za)
    dictionary['@@lap@@'] = str(lap)
    dictionary['@@apn@@'] = str(apn)
    dictionary['@@pap@@'] = str(pap)
    dictionary['@@ln@@'] = str(ln)
    dictionary['@@lapn@@'] = str(lapn)
    dictionary['@@pn@@'] = str(pn)
    dictionary['@@papn@@'] = str(papn)
    dictionary['@@lapap@@'] = str(lapap)
    dictionary['@@apap@@'] = str(apap)
    dictionary['@@hw@@'] = str(hw)
    dictionary['@@lww@@'] = str(lww)
    dictionary['@@xx@@'] = str(xx)
    dictionary['@@zw@@'] = str(zw)
    dictionary['@@x@@'] = str(x)
    dictionary['@@lw@@'] = str(lw)
#
    ocup=float(dictionary.get('@@ocup@@'))
    dpe=116.45*(ocup**-0.923)
    dictionary['@@dpe@@'] = str(dpe)
#
    upar=float(dictionary.get('@@upar@@'))
    rpar=(1/upar)-0.0745
    dictionary['@@rpar@@'] = str(rpar)
#
    ctpar=float(dictionary.get('@@ctpar@@'))
    dpar=(1000*ctpar-35441)/57.50
    dictionary['@@dpar@@'] = str(dpar)
#
    ucob=float(dictionary.get('@@ucob@@'))
    rcob=(1/ucob)-0.06556
    dictionary['@@rcob@@'] = str(rcob)
#
    ctcob=float(dictionary.get('@@ctcob@@'))
    dcob=(1000*ctcob-12768)/100
    dictionary['@@dcob@@'] = str(dcob)
#
    ctint=float(dictionary.get('@@ctint@@'))
    dint=1000*ctint/50
    dictionary['@@dint@@'] = str(dint)
#
    pavtos=float(dictionary.get('@@pavtos@@'))
    pavtostipos=pavtos-2
    dictionary['@@pavtos_tipos@@'] = str(pavtostipos)
#
    if dictionary.get('@@tipo_vent@@') == '0':
        dictionary['@@system_t1_p1@@'] = 'System_VAC_T1_p1.txt'
        dictionary['@@system_t1_p2@@'] = 'System_VAC_T1_p2.txt'
        dictionary['@@system_t2_p1@@'] = 'System_VAC_T2_p1.txt'
        dictionary['@@system_t2_p2@@'] = 'System_VAC_T2_p2.txt'
        dictionary['@@system_t3_p1@@'] = 'System_VAC_T3_p1.txt'
        dictionary['@@system_t3_p2@@'] = 'System_VAC_T3_p2.txt'
        dictionary['@@system_t4_p1@@'] = 'System_VAC_T4_p1.txt'
        dictionary['@@system_t4_p2@@'] = 'System_VAC_T4_p2.txt'
        dictionary['@@system_t5_p1@@'] = 'System_VAC_T5_p1.txt'
        dictionary['@@system_t5_p2@@'] = 'System_VAC_T5_p2.txt'
        dictionary['@@system_m1_p1@@'] = 'System_VAC_M1_p1.txt'
        dictionary['@@system_m1_p2@@'] = 'System_VAC_M1_p2.txt'
        dictionary['@@system_m2_p1@@'] = 'System_VAC_M2_p1.txt'
        dictionary['@@system_m2_p2@@'] = 'System_VAC_M2_p2.txt'
        dictionary['@@system_m3_p1@@'] = 'System_VAC_M3_p1.txt'
        dictionary['@@system_m3_p2@@'] = 'System_VAC_M3_p2.txt'
        dictionary['@@system_m4_p1@@'] = 'System_VAC_M4_p1.txt'
        dictionary['@@system_m4_p2@@'] = 'System_VAC_M4_p2.txt'
        dictionary['@@system_m5_p1@@'] = 'System_VAC_M5_p1.txt'
        dictionary['@@system_m5_p2@@'] = 'System_VAC_M5_p2.txt'
        dictionary['@@system_a1_p1@@'] = 'System_VAC_A1_p1.txt'
        dictionary['@@system_a1_p2@@'] = 'System_VAC_A1_p2.txt'
        dictionary['@@system_a2_p1@@'] = 'System_VAC_A2_p1.txt'
        dictionary['@@system_a2_p2@@'] = 'System_VAC_A2_p2.txt'
        dictionary['@@system_a3_p1@@'] = 'System_VAC_A3_p1.txt'
        dictionary['@@system_a3_p2@@'] = 'System_VAC_A3_p2.txt'
        dictionary['@@system_a4_p1@@'] = 'System_VAC_A4_p1.txt'
        dictionary['@@system_a4_p2@@'] = 'System_VAC_A4_p2.txt'
        dictionary['@@system_a5_p1@@'] = 'System_VAC_A5_p1.txt'
        dictionary['@@system_a5_p2@@'] = 'System_VAC_A5_p2.txt'
        dictionary['@@system_p3@@'] = 'System_VAC_p3.txt'
        dictionary['@@system_p4@@'] = 'System_VAC_p4.txt'
    elif dictionary.get('@@tipo_vent@@') == '1':
        dictionary['@@system_t1_p1@@'] = 'System_VAV_T1_p1.txt'
        dictionary['@@system_t1_p2@@'] = 'System_VAV_T1_p2.txt'
        dictionary['@@system_t2_p1@@'] = 'System_VAV_T2_p1.txt'
        dictionary['@@system_t2_p2@@'] = 'System_VAV_T2_p2.txt'
        dictionary['@@system_t3_p1@@'] = 'System_VAV_T3_p1.txt'
        dictionary['@@system_t3_p2@@'] = 'System_VAV_T3_p2.txt'
        dictionary['@@system_t4_p1@@'] = 'System_VAV_T4_p1.txt'
        dictionary['@@system_t4_p2@@'] = 'System_VAV_T4_p2.txt'
        dictionary['@@system_t5_p1@@'] = 'System_VAV_T5_p1.txt'
        dictionary['@@system_t5_p2@@'] = 'System_VAV_T5_p2.txt'
        dictionary['@@system_m1_p1@@'] = 'System_VAV_M1_p1.txt'
        dictionary['@@system_m1_p2@@'] = 'System_VAV_M1_p2.txt'
        dictionary['@@system_m2_p1@@'] = 'System_VAV_M2_p1.txt'
        dictionary['@@system_m2_p2@@'] = 'System_VAV_M2_p2.txt'
        dictionary['@@system_m3_p1@@'] = 'System_VAV_M3_p1.txt'
        dictionary['@@system_m3_p2@@'] = 'System_VAV_M3_p2.txt'
        dictionary['@@system_m4_p1@@'] = 'System_VAV_M4_p1.txt'
        dictionary['@@system_m4_p2@@'] = 'System_VAV_M4_p2.txt'
        dictionary['@@system_m5_p1@@'] = 'System_VAV_M5_p1.txt'
        dictionary['@@system_m5_p2@@'] = 'System_VAV_M5_p2.txt'
        dictionary['@@system_a1_p1@@'] = 'System_VAV_A1_p1.txt'
        dictionary['@@system_a1_p2@@'] = 'System_VAV_A1_p2.txt'
        dictionary['@@system_a2_p1@@'] = 'System_VAV_A2_p1.txt'
        dictionary['@@system_a2_p2@@'] = 'System_VAV_A2_p2.txt'
        dictionary['@@system_a3_p1@@'] = 'System_VAV_A3_p1.txt'
        dictionary['@@system_a3_p2@@'] = 'System_VAV_A3_p2.txt'
        dictionary['@@system_a4_p1@@'] = 'System_VAV_A4_p1.txt'
        dictionary['@@system_a4_p2@@'] = 'System_VAV_A4_p2.txt'
        dictionary['@@system_a5_p1@@'] = 'System_VAV_A5_p1.txt'
        dictionary['@@system_a5_p2@@'] = 'System_VAV_A5_p2.txt'
        dictionary['@@system_p3@@'] = 'System_VAV_p3.txt'
        dictionary['@@system_p4@@'] = 'System_VAV_p4.txt'

    if dictionary.get('@@tipo_vent@@') == '0':
        dictionary['@@zone_t1_p1@@'] = 'Zone_VAC_T1_p1.txt'
        dictionary['@@zone_t2_p1@@'] = 'Zone_VAC_T2_p1.txt'
        dictionary['@@zone_t3_p1@@'] = 'Zone_VAC_T3_p1.txt'
        dictionary['@@zone_t4_p1@@'] = 'Zone_VAC_T4_p1.txt'
        dictionary['@@zone_t5_p1@@'] = 'Zone_VAC_T5_p1.txt'
        dictionary['@@zone_m1_p1@@'] = 'Zone_VAC_M1_p1.txt'
        dictionary['@@zone_m2_p1@@'] = 'Zone_VAC_M2_p1.txt'
        dictionary['@@zone_m3_p1@@'] = 'Zone_VAC_M3_p1.txt'
        dictionary['@@zone_m4_p1@@'] = 'Zone_VAC_M4_p1.txt'
        dictionary['@@zone_m5_p1@@'] = 'Zone_VAC_M5_p1.txt'
        dictionary['@@zone_a1_p1@@'] = 'Zone_VAC_A1_p1.txt'
        dictionary['@@zone_a2_p1@@'] = 'Zone_VAC_A2_p1.txt'
        dictionary['@@zone_a3_p1@@'] = 'Zone_VAC_A3_p1.txt'
        dictionary['@@zone_a4_p1@@'] = 'Zone_VAC_A4_p1.txt'
        dictionary['@@zone_a5_p1@@'] = 'Zone_VAC_A5_p1.txt'
        dictionary['@@zone_p2@@'] = 'Zone_VAC_p2.txt'
        dictionary['@@zone_p3@@'] = 'Zone_VAC_p3.txt'
    elif dictionary.get('@@tipo_vent@@') == '1':
        dictionary['@@zone_t1_p1@@'] = 'Zone_VAV_T1_p1.txt'
        dictionary['@@zone_t2_p1@@'] = 'Zone_VAV_T2_p1.txt'
        dictionary['@@zone_t3_p1@@'] = 'Zone_VAV_T3_p1.txt'
        dictionary['@@zone_t4_p1@@'] = 'Zone_VAV_T4_p1.txt'
        dictionary['@@zone_t5_p1@@'] = 'Zone_VAV_T5_p1.txt'
        dictionary['@@zone_m1_p1@@'] = 'Zone_VAV_M1_p1.txt'
        dictionary['@@zone_m2_p1@@'] = 'Zone_VAV_M2_p1.txt'
        dictionary['@@zone_m3_p1@@'] = 'Zone_VAV_M3_p1.txt'
        dictionary['@@zone_m4_p1@@'] = 'Zone_VAV_M4_p1.txt'
        dictionary['@@zone_m5_p1@@'] = 'Zone_VAV_M5_p1.txt'
        dictionary['@@zone_a1_p1@@'] = 'Zone_VAV_A1_p1.txt'
        dictionary['@@zone_a2_p1@@'] = 'Zone_VAV_A2_p1.txt'
        dictionary['@@zone_a3_p1@@'] = 'Zone_VAV_A3_p1.txt'
        dictionary['@@zone_a4_p1@@'] = 'Zone_VAV_A4_p1.txt'
        dictionary['@@zone_a5_p1@@'] = 'Zone_VAV_A5_p1.txt'
        dictionary['@@zone_p2@@'] = 'Zone_VAV_p2.txt'
	if dictionary.get('@@eco_recup@@') == '1':
            dictionary['@@zone_p3@@'] = 'Zone_VAV_p3_65.txt'
	elif dictionary.get('@@eco_recup@@') == '0':
            dictionary['@@zone_p3@@'] = 'Zone_VAV_p3_20.txt'
	elif dictionary.get('@@eco_recup@@') == '2':
            dictionary['@@zone_p3@@'] = 'Zone_VAV_p3_20.txt'
        
    if dictionary.get('@@renova@@') == '0':
        dictionary['@@renova_pessoa@@'] = '0.0025'
        dictionary['@@renova_area@@'] = '0.0003'
    elif dictionary.get('@@renova@@') == '1':
        dictionary['@@renova_pessoa@@'] = '0.0031'
        dictionary['@@renova_area@@'] = '0.0004'
    elif dictionary.get('@@renova@@') == '2':
        dictionary['@@renova_pessoa@@'] = '0.0038'
        dictionary['@@renova_area@@'] = '0.0005'

    if dictionary.get('@@eco_recup@@') == '0':
        dictionary['@@ciclo_eco@@'] = 'DifferentialEnthalpy'
        dictionary['@@recup_calor@@'] = 'None'
    elif dictionary.get('@@eco_recup@@') == '1':
        dictionary['@@ciclo_eco@@'] = 'NoEconomizer'
        dictionary['@@recup_calor@@'] = 'Enthalpy'
    elif dictionary.get('@@eco_recup@@') == '2':
        dictionary['@@ciclo_eco@@'] = 'NoEconomizer'
        dictionary['@@recup_calor@@'] = 'None'
        
    if dictionary.get('@@t_bombas@@') == '0':
        dictionary['@@tipo_bombas@@'] = 'ConstantPrimaryVariableSecondary'
    elif dictionary.get('@@t_bombas@@') == '1':
        dictionary['@@tipo_bombas@@'] = 'ConstantPrimaryNoSecondary'
    elif dictionary.get('@@t_bombas@@') == '2':
        dictionary['@@tipo_bombas@@'] = 'VariablePrimaryNoSecondary'
        
    if dictionary.get('@@c_not@@') == '0':
        dictionary['@@ciclo_not@@'] = 'StayOff'
    elif dictionary.get('@@c_not@@') == '1':
        dictionary['@@ciclo_not@@'] = 'CycleOnAny'
        
    if dictionary.get('@@r_ag@@') == '0':
        dictionary['@@reset_ag@@'] = 'None'
    elif dictionary.get('@@r_ag@@') == '1':
        dictionary['@@reset_ag@@'] = 'OutdoorAirTemperatureReset' 

    if dictionary.get('@@tipo_bombas@@') == 'ConstantPrimaryVariableSecondary':
	dictionary['@@pressao_bomba_prim@@'] = '150000'
        pt=float(dictionary.get('@@pressao_bomba_ag@@'))
        ps=pt-150000
        dictionary['@@pressao_bomba_sec@@'] = str(ps)
    elif dictionary.get('@@tipo_bombas@@') == 'ConstantPrimaryNoSecondary':
        pt=float(dictionary.get('@@pressao_bomba_ag@@')) 
        dictionary['@@pressao_bomba_prim@@'] = str(pt)
        dictionary['@@pressao_bomba_sec@@'] = '0'
    elif dictionary.get('@@tipo_bombas@@') == 'VariablePrimaryNoSecondary':
        pt=float(dictionary.get('@@pressao_bomba_ag@@'))
        dictionary['@@pressao_bomba_prim@@'] = str(pt)
        dictionary['@@pressao_bomba_sec@@'] = '0'

    if dictionary.get('@@horas@@') == '8':
        dictionary['@@inicio@@'] = '9:00'
        dictionary['@@fim@@'] = '17:00'
    elif dictionary.get('@@horas@@') == '9':
        dictionary['@@inicio@@'] = '8:00'
        dictionary['@@fim@@'] = '17:00'
    elif dictionary.get('@@horas@@') == '10':
        dictionary['@@inicio@@'] = '8:00'
        dictionary['@@fim@@'] = '18:00'
    elif dictionary.get('@@horas@@') == '11':
        dictionary['@@inicio@@'] = '7:00'
        dictionary['@@fim@@'] = '18:00'
    elif dictionary.get('@@horas@@') == '12':
        dictionary['@@inicio@@'] = '7:00'
        dictionary['@@fim@@'] = '19:00'
    elif dictionary.get('@@horas@@') == '13':
        dictionary['@@inicio@@'] = '7:00'
        dictionary['@@fim@@'] = '20:00'
    elif dictionary.get('@@horas@@') == '14':
        dictionary['@@inicio@@'] = '7:00'
        dictionary['@@fim@@'] = '21:00'
    elif dictionary.get('@@horas@@') == '15':
        dictionary['@@inicio@@'] = '7:00'
        dictionary['@@fim@@'] = '22:00'
    elif dictionary.get('@@horas@@') == '16':
        dictionary['@@inicio@@'] = '7:00'
        dictionary['@@fim@@'] = '23:00'
#      
    if dictionary.get('@@clima@@') == '1':
        dictionary['@@epw@@'] = 'epw1.txt'
    elif dictionary.get('@@clima@@') == '2':
        dictionary['@@epw@@'] = 'epw2.txt'
    elif dictionary.get('@@clima@@') == '3':
        dictionary['@@epw@@'] = 'epw3.txt'
    elif dictionary.get('@@clima@@') == '4':
        dictionary['@@epw@@'] = 'epw4.txt'
    elif dictionary.get('@@clima@@') == '5':
        dictionary['@@epw@@'] = 'epw5.txt'
    elif dictionary.get('@@clima@@') == '6':
        dictionary['@@epw@@'] = 'epw6.txt'
    elif dictionary.get('@@clima@@') == '7':
        dictionary['@@epw@@'] = 'epw7.txt'
    elif dictionary.get('@@clima@@') == '8':
        dictionary['@@epw@@'] = 'epw8.txt'
    elif dictionary.get('@@clima@@') == '9':
        dictionary['@@epw@@'] = 'epw9.txt'
    elif dictionary.get('@@clima@@') == '10':
        dictionary['@@epw@@'] = 'epw10.txt'
    elif dictionary.get('@@clima@@') == '11':
        dictionary['@@epw@@'] = 'epw11.txt'
    elif dictionary.get('@@clima@@') == '12':
        dictionary['@@epw@@'] = 'epw12.txt'
    elif dictionary.get('@@clima@@') == '13':
        dictionary['@@epw@@'] = 'epw13.txt'
    elif dictionary.get('@@clima@@') == '14':
        dictionary['@@epw@@'] = 'epw14.txt'
    elif dictionary.get('@@clima@@') == '15':
        dictionary['@@epw@@'] = 'epw15.txt'
    elif dictionary.get('@@clima@@') == '16':
        dictionary['@@epw@@'] = 'epw16.txt'
    elif dictionary.get('@@clima@@') == '17':
        dictionary['@@epw@@'] = 'epw17.txt'
    elif dictionary.get('@@clima@@') == '18':
        dictionary['@@epw@@'] = 'epw18.txt'

    if dictionary.get('@@nch@@') == '1':
        dictionary['@@arranjo_bombas@@'] = 'SinglePump'
        if dictionary.get('@@chil@@') == '0':
            dictionary['@@chillers@@'] = 'chiller00.txt'
        elif dictionary.get('@@chil@@') == '1':
            dictionary['@@chillers@@'] = 'chiller01.txt'
        elif dictionary.get('@@chil@@') == '2':
            dictionary['@@chillers@@'] = 'chiller02.txt'        
        elif dictionary.get('@@chil@@') == '3':
            dictionary['@@chillers@@'] = 'chiller03.txt' 
        elif dictionary.get('@@chil@@') == '4':
            dictionary['@@chillers@@'] = 'chiller04.txt'
        elif dictionary.get('@@chil@@') == '5':
            dictionary['@@chillers@@'] = 'chiller05.txt'
        elif dictionary.get('@@chil@@') == '6':
            dictionary['@@chillers@@'] = 'chiller06.txt'
        elif dictionary.get('@@chil@@') == '7':
            dictionary['@@chillers@@'] = 'chiller07.txt'
        elif dictionary.get('@@chil@@') == '8':
            dictionary['@@chillers@@'] = 'chiller08.txt'
        elif dictionary.get('@@chil@@') == '9':
            dictionary['@@chillers@@'] = 'chiller09.txt'
        elif dictionary.get('@@chil@@') == '10':
            dictionary['@@chillers@@'] = 'chiller10.txt'
        elif dictionary.get('@@chil@@') == '11':
            dictionary['@@chillers@@'] = 'chiller11.txt'
        elif dictionary.get('@@chil@@') == '12':
            dictionary['@@chillers@@'] = 'chiller12.txt'        
        elif dictionary.get('@@chil@@') == '13':
            dictionary['@@chillers@@'] = 'chiller13.txt' 
        elif dictionary.get('@@chil@@') == '14':
            dictionary['@@chillers@@'] = 'chiller14.txt'
        elif dictionary.get('@@chil@@') == '15':
            dictionary['@@chillers@@'] = 'chiller15.txt'
        elif dictionary.get('@@chil@@') == '16':
            dictionary['@@chillers@@'] = 'chiller16.txt'
        elif dictionary.get('@@chil@@') == '17':
            dictionary['@@chillers@@'] = 'chiller17.txt'
        elif dictionary.get('@@chil@@') == '18':
            dictionary['@@chillers@@'] = 'chiller18.txt'
        elif dictionary.get('@@chil@@') == '19':
            dictionary['@@chillers@@'] = 'chiller19.txt'
        elif dictionary.get('@@chil@@') == '20':
            dictionary['@@chillers@@'] = 'chiller20.txt'
        elif dictionary.get('@@chil@@') == '21':
            dictionary['@@chillers@@'] = 'chiller21.txt'
        elif dictionary.get('@@chil@@') == '22':
            dictionary['@@chillers@@'] = 'chiller22.txt'        
        elif dictionary.get('@@chil@@') == '23':
            dictionary['@@chillers@@'] = 'chiller23.txt' 
        elif dictionary.get('@@chil@@') == '24':
            dictionary['@@chillers@@'] = 'chiller24.txt'
        elif dictionary.get('@@chil@@') == '25':
            dictionary['@@chillers@@'] = 'chiller25.txt'
        elif dictionary.get('@@chil@@') == '26':
            dictionary['@@chillers@@'] = 'chiller26.txt'
        elif dictionary.get('@@chil@@') == '27':
            dictionary['@@chillers@@'] = 'chiller27.txt'
        elif dictionary.get('@@chil@@') == '28':
            dictionary['@@chillers@@'] = 'chiller28.txt'
        elif dictionary.get('@@chil@@') == '29':
            dictionary['@@chillers@@'] = 'chiller29.txt'
        elif dictionary.get('@@chil@@') == '30':
            dictionary['@@chillers@@'] = 'chiller30.txt'
        elif dictionary.get('@@chil@@') == '31':
            dictionary['@@chillers@@'] = 'chiller31.txt'
        elif dictionary.get('@@chil@@') == '32':
            dictionary['@@chillers@@'] = 'chiller32.txt'        
        elif dictionary.get('@@chil@@') == '33':
            dictionary['@@chillers@@'] = 'chiller33.txt' 
        elif dictionary.get('@@chil@@') == '34':
            dictionary['@@chillers@@'] = 'chiller34.txt'
        elif dictionary.get('@@chil@@') == '35':
            dictionary['@@chillers@@'] = 'chiller35.txt'
        elif dictionary.get('@@chil@@') == '36':
            dictionary['@@chillers@@'] = 'chiller36.txt'
        elif dictionary.get('@@chil@@') == '37':
            dictionary['@@chillers@@'] = 'chiller37.txt'
        elif dictionary.get('@@chil@@') == '38':
            dictionary['@@chillers@@'] = 'chiller38.txt'
        elif dictionary.get('@@chil@@') == '39':
            dictionary['@@chillers@@'] = 'chiller39.txt'
    elif dictionary.get('@@nch@@') == '2':
        dictionary['@@arranjo_bombas@@'] = 'TwoHeaderedPumps'
        if dictionary.get('@@chil@@') == '0':
            dictionary['@@chillers@@'] = '2chiller00.txt'
        elif dictionary.get('@@chil@@') == '1':
            dictionary['@@chillers@@'] = '2chiller01.txt'
        elif dictionary.get('@@chil@@') == '2':
            dictionary['@@chillers@@'] = '2chiller02.txt'        
        elif dictionary.get('@@chil@@') == '3':
            dictionary['@@chillers@@'] = '2chiller03.txt' 
        elif dictionary.get('@@chil@@') == '4':
            dictionary['@@chillers@@'] = '2chiller04.txt'
        elif dictionary.get('@@chil@@') == '5':
            dictionary['@@chillers@@'] = '2chiller05.txt'
        elif dictionary.get('@@chil@@') == '6':
            dictionary['@@chillers@@'] = '2chiller06.txt'
        elif dictionary.get('@@chil@@') == '7':
            dictionary['@@chillers@@'] = '2chiller07.txt'
        elif dictionary.get('@@chil@@') == '8':
            dictionary['@@chillers@@'] = '2chiller08.txt'
        elif dictionary.get('@@chil@@') == '9':
            dictionary['@@chillers@@'] = '2chiller09.txt'
        elif dictionary.get('@@chil@@') == '10':
            dictionary['@@chillers@@'] = '2chiller10.txt'
        elif dictionary.get('@@chil@@') == '11':
            dictionary['@@chillers@@'] = '2chiller11.txt'
        elif dictionary.get('@@chil@@') == '12':
            dictionary['@@chillers@@'] = '2chiller12.txt'        
        elif dictionary.get('@@chil@@') == '13':
            dictionary['@@chillers@@'] = '2chiller13.txt' 
        elif dictionary.get('@@chil@@') == '14':
            dictionary['@@chillers@@'] = '2chiller14.txt'
        elif dictionary.get('@@chil@@') == '15':
            dictionary['@@chillers@@'] = '2chiller15.txt'
        elif dictionary.get('@@chil@@') == '16':
            dictionary['@@chillers@@'] = '2chiller16.txt'
        elif dictionary.get('@@chil@@') == '17':
            dictionary['@@chillers@@'] = '2chiller17.txt'
        elif dictionary.get('@@chil@@') == '18':
            dictionary['@@chillers@@'] = '2chiller18.txt'
        elif dictionary.get('@@chil@@') == '19':
            dictionary['@@chillers@@'] = '2chiller19.txt'
        elif dictionary.get('@@chil@@') == '20':
            dictionary['@@chillers@@'] = '2chiller20.txt'
        elif dictionary.get('@@chil@@') == '21':
            dictionary['@@chillers@@'] = '2chiller21.txt'
        elif dictionary.get('@@chil@@') == '22':
            dictionary['@@chillers@@'] = '2chiller22.txt'        
        elif dictionary.get('@@chil@@') == '23':
            dictionary['@@chillers@@'] = '2chiller23.txt' 
        elif dictionary.get('@@chil@@') == '24':
            dictionary['@@chillers@@'] = '2chiller24.txt'
        elif dictionary.get('@@chil@@') == '25':
            dictionary['@@chillers@@'] = '2chiller25.txt'
        elif dictionary.get('@@chil@@') == '26':
            dictionary['@@chillers@@'] = '2chiller26.txt'
        elif dictionary.get('@@chil@@') == '27':
            dictionary['@@chillers@@'] = '2chiller27.txt'
        elif dictionary.get('@@chil@@') == '28':
            dictionary['@@chillers@@'] = '2chiller28.txt'
        elif dictionary.get('@@chil@@') == '29':
            dictionary['@@chillers@@'] = '2chiller29.txt'
        elif dictionary.get('@@chil@@') == '30':
            dictionary['@@chillers@@'] = '2chiller30.txt'
        elif dictionary.get('@@chil@@') == '31':
            dictionary['@@chillers@@'] = '2chiller31.txt'
        elif dictionary.get('@@chil@@') == '32':
            dictionary['@@chillers@@'] = '2chiller32.txt'        
        elif dictionary.get('@@chil@@') == '33':
            dictionary['@@chillers@@'] = '2chiller33.txt' 
        elif dictionary.get('@@chil@@') == '34':
            dictionary['@@chillers@@'] = '2chiller34.txt'
        elif dictionary.get('@@chil@@') == '35':
            dictionary['@@chillers@@'] = '2chiller35.txt'
        elif dictionary.get('@@chil@@') == '36':
            dictionary['@@chillers@@'] = '2chiller36.txt'
        elif dictionary.get('@@chil@@') == '37':
            dictionary['@@chillers@@'] = '2chiller37.txt'
        elif dictionary.get('@@chil@@') == '38':
            dictionary['@@chillers@@'] = '2chiller38.txt'
        elif dictionary.get('@@chil@@') == '39':
            dictionary['@@chillers@@'] = '2chiller39.txt'
    elif dictionary.get('@@nch@@') == '3':
        dictionary['@@arranjo_bombas@@'] = 'ThreeHeaderedPumps'
        if dictionary.get('@@chil@@') == '0':
            dictionary['@@chillers@@'] = '3chiller00.txt'
        elif dictionary.get('@@chil@@') == '1':
            dictionary['@@chillers@@'] = '3chiller01.txt'
        elif dictionary.get('@@chil@@') == '2':
            dictionary['@@chillers@@'] = '3chiller02.txt'        
        elif dictionary.get('@@chil@@') == '3':
            dictionary['@@chillers@@'] = '3chiller03.txt' 
        elif dictionary.get('@@chil@@') == '4':
            dictionary['@@chillers@@'] = '3chiller04.txt'
        elif dictionary.get('@@chil@@') == '5':
            dictionary['@@chillers@@'] = '3chiller05.txt'
        elif dictionary.get('@@chil@@') == '6':
            dictionary['@@chillers@@'] = '3chiller06.txt'
        elif dictionary.get('@@chil@@') == '7':
            dictionary['@@chillers@@'] = '3chiller07.txt'
        elif dictionary.get('@@chil@@') == '8':
            dictionary['@@chillers@@'] = '3chiller08.txt'
        elif dictionary.get('@@chil@@') == '9':
            dictionary['@@chillers@@'] = '3chiller09.txt'
        elif dictionary.get('@@chil@@') == '10':
            dictionary['@@chillers@@'] = '3chiller10.txt'
        elif dictionary.get('@@chil@@') == '11':
            dictionary['@@chillers@@'] = '3chiller11.txt'
        elif dictionary.get('@@chil@@') == '12':
            dictionary['@@chillers@@'] = '3chiller12.txt'        
        elif dictionary.get('@@chil@@') == '13':
            dictionary['@@chillers@@'] = '3chiller13.txt' 
        elif dictionary.get('@@chil@@') == '14':
            dictionary['@@chillers@@'] = '3chiller14.txt'
        elif dictionary.get('@@chil@@') == '15':
            dictionary['@@chillers@@'] = '3chiller15.txt'
        elif dictionary.get('@@chil@@') == '16':
            dictionary['@@chillers@@'] = '3chiller16.txt'
        elif dictionary.get('@@chil@@') == '17':
            dictionary['@@chillers@@'] = '3chiller17.txt'
        elif dictionary.get('@@chil@@') == '18':
            dictionary['@@chillers@@'] = '3chiller18.txt'
        elif dictionary.get('@@chil@@') == '19':
            dictionary['@@chillers@@'] = '3chiller19.txt'
        elif dictionary.get('@@chil@@') == '20':
            dictionary['@@chillers@@'] = '3chiller20.txt'
        elif dictionary.get('@@chil@@') == '21':
            dictionary['@@chillers@@'] = '3chiller21.txt'
        elif dictionary.get('@@chil@@') == '22':
            dictionary['@@chillers@@'] = '3chiller22.txt'        
        elif dictionary.get('@@chil@@') == '23':
            dictionary['@@chillers@@'] = '3chiller23.txt' 
        elif dictionary.get('@@chil@@') == '24':
            dictionary['@@chillers@@'] = '3chiller24.txt'
        elif dictionary.get('@@chil@@') == '25':
            dictionary['@@chillers@@'] = '3chiller25.txt'
        elif dictionary.get('@@chil@@') == '26':
            dictionary['@@chillers@@'] = '3chiller26.txt'
        elif dictionary.get('@@chil@@') == '27':
            dictionary['@@chillers@@'] = '3chiller27.txt'
        elif dictionary.get('@@chil@@') == '28':
            dictionary['@@chillers@@'] = '3chiller28.txt'
        elif dictionary.get('@@chil@@') == '29':
            dictionary['@@chillers@@'] = '3chiller29.txt'
        elif dictionary.get('@@chil@@') == '30':
            dictionary['@@chillers@@'] = '3chiller30.txt'
        elif dictionary.get('@@chil@@') == '31':
            dictionary['@@chillers@@'] = '3chiller31.txt'
        elif dictionary.get('@@chil@@') == '32':
            dictionary['@@chillers@@'] = '3chiller32.txt'        
        elif dictionary.get('@@chil@@') == '33':
            dictionary['@@chillers@@'] = '3chiller33.txt' 
        elif dictionary.get('@@chil@@') == '34':
            dictionary['@@chillers@@'] = '3chiller34.txt'
        elif dictionary.get('@@chil@@') == '35':
            dictionary['@@chillers@@'] = '3chiller35.txt'
        elif dictionary.get('@@chil@@') == '36':
            dictionary['@@chillers@@'] = '3chiller36.txt'
        elif dictionary.get('@@chil@@') == '37':
            dictionary['@@chillers@@'] = '3chiller37.txt'
        elif dictionary.get('@@chil@@') == '38':
            dictionary['@@chillers@@'] = '3chiller38.txt'
        elif dictionary.get('@@chil@@') == '39':
            dictionary['@@chillers@@'] = '3chiller39.txt'
    elif dictionary.get('@@nch@@') == '4':
        dictionary['@@arranjo_bombas@@'] = 'FourHeaderedPumps'
        if dictionary.get('@@chil@@') == '0':
            dictionary['@@chillers@@'] = '4chiller00.txt'
        elif dictionary.get('@@chil@@') == '1':
            dictionary['@@chillers@@'] = '4chiller01.txt'
        elif dictionary.get('@@chil@@') == '2':
            dictionary['@@chillers@@'] = '4chiller02.txt'        
        elif dictionary.get('@@chil@@') == '3':
            dictionary['@@chillers@@'] = '4chiller03.txt' 
        elif dictionary.get('@@chil@@') == '4':
            dictionary['@@chillers@@'] = '4chiller04.txt'
        elif dictionary.get('@@chil@@') == '5':
            dictionary['@@chillers@@'] = '4chiller05.txt'
        elif dictionary.get('@@chil@@') == '6':
            dictionary['@@chillers@@'] = '4chiller06.txt'
        elif dictionary.get('@@chil@@') == '7':
            dictionary['@@chillers@@'] = '4chiller07.txt'
        elif dictionary.get('@@chil@@') == '8':
            dictionary['@@chillers@@'] = '4chiller08.txt'
        elif dictionary.get('@@chil@@') == '9':
            dictionary['@@chillers@@'] = '4chiller09.txt'
        elif dictionary.get('@@chil@@') == '10':
            dictionary['@@chillers@@'] = '4chiller10.txt'
        elif dictionary.get('@@chil@@') == '11':
            dictionary['@@chillers@@'] = '4chiller11.txt'
        elif dictionary.get('@@chil@@') == '12':
            dictionary['@@chillers@@'] = '4chiller12.txt'        
        elif dictionary.get('@@chil@@') == '13':
            dictionary['@@chillers@@'] = '4chiller13.txt' 
        elif dictionary.get('@@chil@@') == '14':
            dictionary['@@chillers@@'] = '4chiller14.txt'
        elif dictionary.get('@@chil@@') == '15':
            dictionary['@@chillers@@'] = '4chiller15.txt'
        elif dictionary.get('@@chil@@') == '16':
            dictionary['@@chillers@@'] = '4chiller16.txt'
        elif dictionary.get('@@chil@@') == '17':
            dictionary['@@chillers@@'] = '4chiller17.txt'
        elif dictionary.get('@@chil@@') == '18':
            dictionary['@@chillers@@'] = '4chiller18.txt'
        elif dictionary.get('@@chil@@') == '19':
            dictionary['@@chillers@@'] = '4chiller19.txt'
        elif dictionary.get('@@chil@@') == '20':
            dictionary['@@chillers@@'] = '4chiller20.txt'
        elif dictionary.get('@@chil@@') == '21':
            dictionary['@@chillers@@'] = '4chiller21.txt'
        elif dictionary.get('@@chil@@') == '22':
            dictionary['@@chillers@@'] = '4chiller22.txt'        
        elif dictionary.get('@@chil@@') == '23':
            dictionary['@@chillers@@'] = '4chiller23.txt' 
        elif dictionary.get('@@chil@@') == '24':
            dictionary['@@chillers@@'] = '4chiller24.txt'
        elif dictionary.get('@@chil@@') == '25':
            dictionary['@@chillers@@'] = '4chiller25.txt'
        elif dictionary.get('@@chil@@') == '26':
            dictionary['@@chillers@@'] = '4chiller26.txt'
        elif dictionary.get('@@chil@@') == '27':
            dictionary['@@chillers@@'] = '4chiller27.txt'
        elif dictionary.get('@@chil@@') == '28':
            dictionary['@@chillers@@'] = '4chiller28.txt'
        elif dictionary.get('@@chil@@') == '29':
            dictionary['@@chillers@@'] = '4chiller29.txt'
        elif dictionary.get('@@chil@@') == '30':
            dictionary['@@chillers@@'] = '4chiller30.txt'
        elif dictionary.get('@@chil@@') == '31':
            dictionary['@@chillers@@'] = '4chiller31.txt'
        elif dictionary.get('@@chil@@') == '32':
            dictionary['@@chillers@@'] = '4chiller32.txt'        
        elif dictionary.get('@@chil@@') == '33':
            dictionary['@@chillers@@'] = '4chiller33.txt' 
        elif dictionary.get('@@chil@@') == '34':
            dictionary['@@chillers@@'] = '4chiller34.txt'
        elif dictionary.get('@@chil@@') == '35':
            dictionary['@@chillers@@'] = '4chiller35.txt'
        elif dictionary.get('@@chil@@') == '36':
            dictionary['@@chillers@@'] = '4chiller36.txt'
        elif dictionary.get('@@chil@@') == '37':
            dictionary['@@chillers@@'] = '4chiller37.txt'
        elif dictionary.get('@@chil@@') == '38':
            dictionary['@@chillers@@'] = '4chiller38.txt'
        elif dictionary.get('@@chil@@') == '39':
            dictionary['@@chillers@@'] = '4chiller39.txt'


#-------------------------------------------------------------------------------------

def start(csv_file_name, idf_file_name, epw_file_name, folder_name, factors, parameters, samplesSize):
    idf_file = open(idf_file_name)
    idf_file_text = idf_file.read()
    idf_file.close() 

    epw_file = open(epw_file_name)
    epw_file_text = epw_file.read()
    epw_file.close()


    lhd = lhs(len(parameters), samples=samplesSize, criterion='center')
    lhd2 = []
    for i in range(samplesSize):
        row = []
        for j in range(len(parameters)):
            row.append(str(parameters[j][int(discrete(lhd[i][j],len(parameters[j])))-1]))
        lhd2.append(row)
##    generateCSV(factors, lhd, lhd2, csv_file_name, samplesSize)


    csvfile = open(csv_file_name)
    csv_file_as_dict = csv.DictReader(csvfile, delimiter=',')

    folder_number = 0
    for dictionary in csv_file_as_dict:
        complement_the_dictionary(dictionary)

        directory = create_new_folder(folder_name, folder_number)

        create_new_idf_file(directory, idf_file_text, dictionary)
        
        create_new_epw_file(directory, epw_file_text, dictionary)

        # NEXT FOLDER
        folder_number = folder_number + 1
        
    csvfile.close()
    idf_file.close()
    epw_file.close()

#-------------------------------------------------------------------------------------

start(csv_file_name, idf_file_name, epw_file_name, folder_name, _factors, _parameters, _samplesSize)
