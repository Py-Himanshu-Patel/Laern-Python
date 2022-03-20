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
