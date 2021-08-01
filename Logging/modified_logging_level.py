import logging

# logging to console and changing default level of 
logging.basicConfig(level=logging.DEBUG)

# all levels are above debug so everything gets printed to console

logging.debug('This is debug log')

logging.info('This is info log')

logging.warning('This is warning log')

logging.error('This is error log')
