import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        start_time = time.time()
        value = func(*args, **kwargs)
        finish_time = time.time()
        print(f"Finished in {(finish_time-start_time):.7f} sec")
        return value
    return wrapper_decorator


@timer
def test():
    time.sleep(1)


if __name__ == "__main__":
    test()
