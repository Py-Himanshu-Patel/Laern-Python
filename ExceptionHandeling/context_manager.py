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
