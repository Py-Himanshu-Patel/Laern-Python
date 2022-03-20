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
