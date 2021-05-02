'''
Boiler plate code for decorators with argument and without argument
'''

def name(_func=None, *, kw1=None, kw2=None):  # 1
    def decorator_name(func):
        func()

    if _func is None:
        return decorator_name                      # 2
    else:
        return decorator_name(_func)               # 3
