# Python Logger

## Default Logger

Level | When it’s used
--- | ---
DEBUG 		| Detailed information, typically of interest only when diagnosing problems.
INFO  		| Confirmation that things are working as expected.
WARNING		| An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
ERROR		| Due to a more serious problem, the software has not been able to perform some function.
CRITICAL	| A serious error, indicating that the program itself may be unable to continue running.

Before we begin there is a priority to level of logs.

```python
CRITICAL = 50			# highest priority
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0				# lowest priority
```

### Default Logging Level (Console)

```python
import logging

# Default warning level is WARNING 

# log above WARNING and above

# printed in console while running script
logging.warning('This is warning')
logging.error("This is error")

# log below WARNING level

# do not get printed to console
logging.info("This is info")
```

```bash
WARNING:root:This is warning
ERROR:root:This is error
```

### Modified Logging Level (Console)

```python
import logging

# logging to console and changing default level of 
logging.basicConfig(level=logging.DEBUG)

# all levels are above debug so everything gets printed to console

logging.debug('This is debug log')

logging.info('This is info log')

logging.warning('This is warning log')

logging.error('This is error log')
```

### Logging to File

```python
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
```

```bash
DEBUG:root:This is debug log
INFO:root:This is info log
WARNING:root:This is warning log
ERROR:root:This is error log
```

Each time we run this script the logs get appended to file.

### Logging with custom format

```python
import logging

# logging to file with Time:LogLevel:Message format
# for more format https://docs.python.org/3/library/logging.html#formatter-objects
logging.basicConfig(
    filename='example.log', 
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

logging.debug('This is debug log')

logging.info('This is info log')

logging.warning('This is warning log')

logging.error('This is error log')
```

```bash
2021-08-01 22:20:38,605:DEBUG:This is debug log
2021-08-01 22:20:38,606:INFO:This is info log
2021-08-01 22:20:38,606:WARNING:This is warning log
2021-08-01 22:20:38,606:ERROR:This is error log
```

For more format refer [Python Logger Documentation](https://docs.python.org/3/library/logging.html#formatter-objects)
