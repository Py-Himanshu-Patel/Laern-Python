import logging

# Default warning level is WARNING 

# log above WARNING and above

# printed in console while running script
logging.warning('This is warning')
logging.error("This is error")

# log below WARNING level

# do not get printed to console
logging.info("This is info")
