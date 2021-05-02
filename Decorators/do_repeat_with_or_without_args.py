import functools

def repeat(_func=None, *, num_times=2):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat

    if _func is None:
        return decorator_repeat
    else:
        return decorator_repeat(_func)

@repeat(num_times=5)
def printy(name):
	print(f'Hello {name}')

@repeat
def printo(name):
	print(f'Hi {name}')

printy("HP")		# func with arg in decorator
printo("HP")		# func without arg in decorator
