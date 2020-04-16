import os

def missing_cases():
	path_missing = os.listdir(os.getcwd())
	path_missing.remove('resultados')
	path_missing.remove('missing_cases.py')
	
	path = os.listdir('../../tipologia4')

	for element in path:
		if element in path_missing:
			command = "rsync -a /scratch/prjeeesd/marcio.sorgato/tipologia4/%s ./ " % (element)
			os.system(command)

missing_cases()
