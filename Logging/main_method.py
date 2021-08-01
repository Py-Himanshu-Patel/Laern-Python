import logging
import employee

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('logger.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


if __name__ == "__main__":
	e1 = employee.Employee("John", "Doe")
	logger.info("Log of main_method.py")
