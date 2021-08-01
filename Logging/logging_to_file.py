import logging

# logging to console
# logging.basicConfig(level=logging.DEBUG)

# loggin to file
logging.basicConfig(filename='example.log', level=logging.DEBUG)

# try running script with one config commented, else the config 
# which comes first will come to effect (here - console)

logging.debug('This is debug log')

logging.info('This is info log')

logging.warning('This is warning log')

logging.error('This is error log')

# each time we run this script the logs get appended to file
