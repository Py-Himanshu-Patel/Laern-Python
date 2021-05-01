import functools

def decorated_return(func):
	# to preserve the info of func function
	@functools.wraps(func)	
	def wrapper(*args, **kwargs):
		print("Custom Wrapper Script")
		return "Hi! " + func(*args, **kwargs)
	return wrapper

@decorated_return
def greet(name):
	return name.title()

print(greet('HP'))