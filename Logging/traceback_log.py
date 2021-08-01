import logging

logger = logging.getLogger(__name__)

# set this logger to catch all log for DEBUG and above
# we can set level on seperate file handler as well but in case 
# logger is set to level of INFO then even the file handler 
# registered with this logger won't log the records below INFO (like DEBUG)
logger.setLevel(logging.DEBUG)

# formatter for logs
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

# file handler for ERROR level log
# mention the filename where we want to send the logs
file_handler = logging.FileHandler('traceback.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

# stream handler for DEBUG level log
# no parameter means logs send to console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# add all file or stream handler
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def divison(num, den):
	try:
		result = num / den
	except ZeroDivisionError:
		logger.exception("Divison By Zero")
	else:
		return result

logger.debug("This goes to debug log")
logger.debug(f"{divison(5,2)}")
logger.debug(f"{divison(5,0)}")
