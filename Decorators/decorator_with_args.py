def do_twice(func):
	def wrapper_do_twice(*args, **kwargs):
		func(*args, **kwargs)
		func(*args, **kwargs)
	return wrapper_do_twice

@do_twice
def say_whee(name):
	print(f"Hi! {name}")

say_whee("HP")
