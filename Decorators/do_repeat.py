import functools

def repeat(n_times):		# main decorator
	def do_repeat(func):	# sub decorator
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			for _ in range(n_times):
				value = func(*args, **kwargs)
			return value
		return wrapper
	return do_repeat

# pass argument ot decorator itself
@repeat(n_times=5)
def printy(name):
	print(f'Hello {name}')

printy("HP")
