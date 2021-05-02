import functools

def singleton(cls):
	@functools.wraps(cls)
	def wrapper(*args, **kwargs):
		if not wrapper.instance:
			wrapper.instance = cls(*args, **kwargs)
		return wrapper.instance
	wrapper.instance = None
	return wrapper

@singleton
class TheOne:
	pass

# --------- check -------------

firstObj = TheOne()
secObj = TheOne()

print(id(firstObj))
print(id(secObj))

print(firstObj is secObj)
