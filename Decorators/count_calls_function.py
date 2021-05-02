import functools

def count_calls(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		wrapper.num_calls += 1
		print(f"Call {wrapper.num_calls} of {func.__name__}")
		return func(*args, **kwargs)
	wrapper.num_calls = 0
	return wrapper


@count_calls
def SayHi(name):
	print(f"Hi, {name}")

SayHi("HP")
SayHi("HP")
SayHi("HP")

