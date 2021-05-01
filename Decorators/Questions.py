# make a decorator which take a divisor (a function which takes 
# two number and divide them) and prevent divide by zero error

import functools

def decorator(divisor):
	@functools.wraps(divisor)
	def wrapper(*args, **kwargs):
		a,b = args
		if b != 0:
			return divisor(*args)
		return "Denominator is Zero"		
	return wrapper

@decorator
def custom_divisor(a,b):
	return a/b

print(custom_divisor(5,3))
print(custom_divisor(5,0))

