import logging

# logging to file with Time:LogLevel:Message format
# for more format https://docs.python.org/3/library/logging.html#formatter-objects
logging.basicConfig(
	filename='example.log', 
	level=logging.DEBUG,
	format='%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
)

logging.debug('This is debug log')

logging.info('This is info log')

logging.warning('This is warning log')

logging.error('This is error log')
