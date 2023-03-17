import logging
import logging.config
from datetime import datetime,date

# ConfigureLogger('DEBUG', f'./Log/{Now.strftime("%Y-%m-%d")}.log')
def ConfigureLogger(level: str, log_path: str):
	if type(log_path) != str:
		raise TypeError(f"log_path type is {type(log_path)} should be str")
	if type(level) != str:
		raise TypeError(f"level type is {type(level)} should be str")
	if level not in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'):
		raise ValueError(f"level str {level} is invalid aloud values are DEBUG, INFO, WARNING, ERROR, CRITICAL")
	logging.config.dictConfig({
		'version': 1,
		'formatters': {'default': {'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S %Z'}},
		'handlers': {
			'console': {'level': level, 'class': 'logging.StreamHandler', 'formatter': 'default', 'stream': 'ext://sys.stdout'},
			'file': {'level': level, 'class': 'logging.FileHandler', 'filename': log_path}
		},
		'loggers': {'default': {'level': level,'handlers': ['console', 'file']}},
		'disable_existing_loggers': False
	})
	return logging.getLogger("default")

def FindReplaceList(find, replace, inputList: list):
	if type(inputList) != list:
		raise TypeError(f'inputList type is {type(inputList)} should be list')
	try:
		return [replace if x == find else x for x in inputList]
	except Exception as err:
		logging.error(err)
		raise(err)

def AddMonths(inputDate: date, addMonths: int = 1) -> date:
	# time date max year is 9999
	if type(inputDate) != date:
		raise TypeError(f'inputDate type is {type(inputDate)} should be date')
	if type(addMonths) != int:
		raise TypeError(f'addMonths type is {type(addMonths)} should be int')
	if addMonths < 1:
		raise ValueError(f'addMonths is {addMonths} and cant be less then 1')
	try:
		NewYear = inputDate.year
		NewMonth = inputDate.month + addMonths
		if NewMonth > 12:
			TempMonths = NewMonth%12
			NewYear = NewYear+(NewMonth-TempMonths)//12
			NewMonth = TempMonths
		return inputDate.replace(year=NewYear, month=NewMonth)
	except Exception as err:
		logging.error(err)
		raise(err)
