import logging

# name is a string : equals __main__ when we exe this file and 
# equals employee.py when exe from another module
logger = logging.getLogger(__name__)

# set level of logger instance
logger.setLevel(logging.INFO)
# set a format for logs
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
# make a file handler 
file_handler = logging.FileHandler('employee.log')
# add formatter to file handler
file_handler.setFormatter(formatter)
# add formatter to logger
logger.addHandler(file_handler)


class Employee:
	def __init__(self, first_name, last_name) -> None:
		self.first_name = first_name
		self.last_name = last_name

		# update from logging lib to logger instance
		logger.info(f"Employee Created : {self.get_name()}")

	def get_email(self):
		return f"{self.first_name}.{self.last_name}@company.com"

	def get_name(self):
		return f"{self.first_name} {self.last_name}"


if __name__ == "__main__":
	e1 = Employee('Jane','Stuart')
