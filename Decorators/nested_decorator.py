from timer import timer
import functools

def hello_decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        value = func(*args, **kwargs)
        print("Hello")
        return value
    return wrapper_decorator


@timer
@hello_decorator
def print_arg(*args):
	print(args)

print_arg("HP")
