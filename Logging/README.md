# Python Logger

Thanks to [Corey Schafers - Python Tutorial: Logging Advanced](https://www.youtube.com/watch?v=jxmzY9soFXg&list=PLKrrYuFe8YTHrcgDKeHV4XAnkcIEAkEWs&index=40&ab_channel=CoreySchafer)

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

## Logging with different files

Till now we have logged only one module. Lets check how to log different modules. Here we put a logger for a class and log the object creation.

### Single Logger instaces

```python
# employee.py

import logging

logging.basicConfig(
    filename='logger.log', 
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
)


class Employee:
    def __init__(self, first_name, last_name) -> None:
        self.first_name = first_name
        self.last_name = last_name

        # update from logging lib to logger instance
        logging.info(f"Employee Created : {self.get_name()}")

    def get_email(self):
        return f"{self.first_name}.{self.last_name}@company.com"

    def get_name(self):
        return f"{self.first_name} {self.last_name}"

if __name__ == "__main__":
    e1 = Employee('Jane','Stuart')
```

```bash
# logger.log
2021-08-02 00:08:36,834:INFO:root:Employee Created : Jane Stuart
```

Now what if we run this file from a different module. Lets creat another module which actually call this class. A note here even though we imported the `employee` module in `main_method` module when we execute the code the execution goes to `employee` module as well there it find the configuration of logger and hence the file which get logged is `employee.py` and not `main_method.py` one.

```python
import logging
import employee

logging.basicConfig(
    filename='logger.log', 
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
)

if __name__ == "__main__":
    e1 = employee.Employee("John", "Doe")
```

```bash
2021-08-02 00:10:02,707:INFO:root:Employee Created : John Doe
```

### Multiple Logger instaces

Now lets use seperate logger for each module so that we can configure them seperately. See the name of method logger getting logged as 

```python
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
```

When called from `employee.py`

```bash
# employee.log
2021-08-02 00:22:51,370:INFO:__main__:Employee Created : Jane Stuart
```

When run from main method

```python
# main_method.py
import logging
import employee

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('employee.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


if __name__ == "__main__":
    e1 = employee.Employee("John", "Doe")
    logger.info("Log of main_method.py")
```

```bash
# employee.log
2021-08-02 01:17:50,932:INFO:employee:Employee Created : John Doe
```

```bash
# logger.log
2021-08-02 01:17:50,933:INFO:__main__:Log of main_method.py
```

## Traceback in Logger

```python
# traceback_log.py
import logging

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('traceback.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def divison(num, den):
    try:
        result = num / den
    except ZeroDivisionError:
        logger.exception("Divison By Zero")
    else:
        return result


print(divison(5,2))
print(divison(5,0))
```

```bash
# console
2.5
None
```

```bash
# traceback.log
2021-08-02 01:24:31,543:ERROR:__main__:Divison By Zero
Traceback (most recent call last):
  File "/home/himanshu/HP/dev/Learn-Python/Logging/traceback_log.py", line 14, in divison
    result = num / den
ZeroDivisionError: division by zero
```

## Handel different level of log in different file or console

```python
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
```

We are able to see the logs on console and stack trace as well since the logger is set to catch all logs for DEBUG and above.

```bash
# console
2021-08-02 02:11:00,844:DEBUG:__main__:This goes to debug log
2021-08-02 02:11:00,844:DEBUG:__main__:2.5
2021-08-02 02:11:00,844:ERROR:__main__:Divison By Zero
Traceback (most recent call last):
  File "/home/himanshu/HP/dev/Learn-Python/Logging/traceback_log.py", line 32, in divison
    result = num / den
ZeroDivisionError: division by zero
2021-08-02 02:11:00,845:DEBUG:__main__:None
```

The ERROR gets noted in log as well.

```bash
# traceback.log
2021-08-02 02:11:00,844:ERROR:__main__:Divison By Zero
Traceback (most recent call last):
  File "/home/himanshu/HP/dev/Learn-Python/Logging/traceback_log.py", line 32, in divison
    result = num / den
ZeroDivisionError: division by zero
```
