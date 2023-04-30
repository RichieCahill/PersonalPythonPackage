from datetime import date
from subprocess import Popen, PIPE
from typing import Tuple

def TypeTest(test_data, test_type: type, error_msg:str):
	if not isinstance(test_data, test_type):
		raise TypeError(error_msg)

# GetLoggerDict('DEBUG', f"./Log/{Now.strftime("%Y-%m-%d")}.log")
def GetLoggerDict(level: str, log_path: str):
	TypeTest(log_path, test_type=str, error_msg=f"log_path type is {type(log_path)} should be str")
	TypeTest(level, test_type=str, error_msg=f"level type is {type(level)} should be str")
	level = level.strip().upper()
	if level not in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'):
		raise ValueError(f"level str {level} is invalid aloud values are DEBUG, INFO, WARNING, ERROR, CRITICAL")
	return{
		'version': 1,
		'formatters': {'default': {'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S %Z'}},
		'handlers': {
			'console': {'level': level, 'class': 'logging.StreamHandler', 'formatter': 'default', 'stream': 'ext://sys.stdout'},
			'file': {'level': level, 'class': 'logging.FileHandler', 'formatter': 'default', 'filename': log_path}
		},
		'loggers': {'default': {'level': level,'handlers': ['console', 'file']}},
    'root': {'level': level, 'handlers': ['console', 'file']},
		'disable_existing_loggers': False
	}

def FindReplaceList(find, replace, inputList: list):
	TypeTest(inputList, test_type=list, error_msg=f"inputList type is {type(inputList)} should be list")
	return [replace if x == find else x for x in inputList]

# time date max year is 9999
def AddMonths(input_date: date, add_months: int = 1) -> date:
	TypeTest(input_date, test_type=date, error_msg=f"input_date type is {type(input_date)} should be date")
	TypeTest(add_months, test_type=int, error_msg=f"add_months type is {type(add_months)} should be int")
	if add_months < 1:
		raise ValueError(f"add_months is {add_months} and cant be less then 1")
	new_year 	= input_date.year
	new_month = input_date.month + add_months
	day 			= input_date.day
	last_day_of_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	if new_month > 12:
		TempMonths = new_month%12
		new_year = new_year+(new_month-TempMonths)//12
		new_month = TempMonths
	if new_year%4 == 0:
		last_day_of_month[2] = 29
	if day > last_day_of_month[new_month]:
		day=last_day_of_month[new_month]
	return input_date.replace(year=new_year, month=new_month, day=day)

def BashWrapper(command: str):
	TypeTest(command, test_type=str, error_msg=f"command type = {command} should be str")
	process = Popen(command.split(), stdout=PIPE)
	output ,error = process.communicate()
	return output.decode(), process.returncode

def TrueBashWrapper(command: str):
	TypeTest(command, test_type=str, error_msg=f"command type = {command} should be str")
	process = Popen(command, shell=True, stdout=PIPE)
	output ,error = process.communicate()
	return output.decode(), process.returncode