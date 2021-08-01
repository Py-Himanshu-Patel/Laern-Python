import logging
import employee

logging.basicConfig(
	filename='logger.log', 
	level=logging.DEBUG,
	format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
)

if __name__ == "__main__":
	e1 = employee.Employee("John", "Doe")
