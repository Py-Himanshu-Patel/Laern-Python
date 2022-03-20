# Advanced Exception Handeling

## Exception handeling with customer exceptions

Make some customer exceptions 

```python
"""
Creating some custom exception
"""

class FileDoNotExistsException(Exception):
	"""
		Throw this error when the file we trying to access do not exist
	"""
	pass

class FileEmptyException(Exception):
	"""
		Throw this exception when File is empty and there is nothing to read 
	"""
	pass


class NotAbleToReadException(Exception):
	"""
		Parent exception to all other exception while reading file
	"""
	pass
```

Making sure the class that open file for reading use these exceptions so that the client class have to deal with only limited number of exceptions.

```bash
"""
Try to read a file which is not present and this will give an exception
Handeling this exception and throwing another customer exceptions is shown here
"""

from customer_exception import FileDoNotExistsException, FileEmptyException, NotAbleToReadException


class ReadData:
	def __init__(self, filename) -> None:
		self.filename = filename

	def readfile(self):
		"""
			throws : NotAbleToReadException and FileDoNotExistsException
		"""
		try:
			file = None				# if any exception in opening file this will remain None
			file = open(self.filename, 'r')
			content = file.read()
			if not content:
				raise FileEmptyException()
			print(content)
		except FileNotFoundError as e:
			# log error and raise another exception 
			raise FileDoNotExistsException(self.filename)
		except FileEmptyException as e:
			raise FileEmptyException(f"{self.filename} is empty")
		except Exception as e:		
			# exception type returned in case of unhandeled exception			
			# So that the user of this module should handle only one type of unhandeled exception
			raise NotAbleToReadException(self.filename)
		finally:
			#  whether or not an exception happends do close the file opened
			if file:
				file.close()


if __name__ == "__main__":
	# throws FileDoNotExistsException and then NotAbleToReadException
	# rd = ReadData('donotexist.txt')
	# rd.readfile()

	# throws FileEmptyException and then NotAbleToReadException
	# rd = ReadData('empty.txt')
	# rd.readfile()

	# do not throw any exception
	rd = ReadData('exists.txt')
	rd.readfile()
```

## Context managers to avoid `finally` block in exception handeling.

```python
"""
Use of context manager to prevent writing finally block in exceptional handeling 
"""

from customer_exception import FileDoNotExistsException, FileEmptyException, NotAbleToReadException


class FileOpener:
	"""
		A context manager to open a read connection to file
	"""
	
	def __init__(self, filename) -> None:
		self.filename = filename

	def __enter__(self):
		self.conn = open(self.filename, 'r')
		return self.conn

	def __exit__(self, type, value, traceback):
		self.conn.close()


class ReadData:
	def __init__(self, filename) -> None:
		self.filename = filename

	def readfile(self):
		"""
			throws : NotAbleToReadException and FileDoNotExistsException
		"""
		try:
			# we don't need finally block as this 'with' context manager closes the file if 
			# any exception occurs or when the block is exited
			with FileOpener(self.filename) as file:	
				content = file.read()
				if not content:
					raise FileEmptyException()
				print(content)
		except FileNotFoundError as e:
			# log error and raise another exception 
			raise FileDoNotExistsException(self.filename)
		except FileEmptyException as e:
			raise FileEmptyException(f"{self.filename} is empty")
		except Exception as e:		
			# exception type returned in case of unhandeled exception			
			# So that the user of this module should handle only one type of unhandeled exception
			raise NotAbleToReadException(self.filename)


if __name__ == "__main__":
	# throws FileDoNotExistsException and then NotAbleToReadException
	# rd = ReadData('donotexist.txt')
	# rd.readfile()

	# throws FileEmptyException and then NotAbleToReadException
	# rd = ReadData('empty.txt')
	# rd.readfile()

	# do not throw any exception
	rd = ReadData('exists.txt')
	rd.readfile()
```

## Retry Decorator

Sometime nothing is wrong and simply retrying a connection or reading a file attempt solves the problem. Let's implement a retry decorator.

```python
import time
from functools import wraps

def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """
    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry

@retry(Exception, tries=3)
def test_fail(text):
    raise Exception("Fail")

test_fail("it works!")
```
