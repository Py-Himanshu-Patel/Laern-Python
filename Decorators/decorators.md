# Decorators

A decorator is a function that takes another function and extends the behavior of the latter function without explicitly modifying it.

In Python, functions are first-class objects. This means that functions can be passed around and used as arguments, just like any other object (string, int, float, list, and so on).

## Inner Functions

It’s possible to define functions inside other functions. Such functions are called inner functions. Here’s an example of a function with two inner functions:

```python
def parent():
    print("Printing from the parent() function")

    def first_child():
        print("Printing from the first_child() function")

    def second_child():
        print("Printing from the second_child() function")

    second_child()
    first_child()
```

## Returning Functions From Functions

Python also allows you to use functions as return values.

```python
def parent(num):
    def first_child():
        return "Hi, I am Emma"

    def second_child():
        return "Call me Liam"

    if num == 1:
        return first_child
    else:
        return second_child

>>> first = parent(1)
>>> second = parent(2)

>>> first
<function parent.<locals>.first_child at 0x7f599f1e2e18>

>>> second
<function parent.<locals>.second_child at 0x7f599dad5268>
```

## Simple Decorators

```python
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_whee():
    print("Whee!")

say_whee()
```

Note: You can name your inner function whatever you want, and a generic name like wrapper() is usually okay. You’ll see a lot of decorators in this article. To keep them apart, we’ll name the inner function with the same name as the decorator but with a wrapper_ prefix.

## Decorators with variables

```python
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice

@do_twice
def say_whee(name):
    print(f"Hi! {name}")

say_whee("HP")
```

## Return value from decorators

```python
def decorated_return(func):
    def wrapper(*args, **kwargs):
        print("Custom Wrapper Script")
        return "Hi! " + func(*args, **kwargs)
    return wrapper

@decorated_return
def greet(name):
    return name.title()

print(greet('HP'))
```

`Introspection` is the ability of an object to know about its own attributes at runtime. For instance, a function knows its own name and documentation

```python
>>> print
<built-in function print>

>>> print.__name__
'print'

>>> help(print)
Help on built-in function print in module builtins:
```

```python
>>> greet.__name__
'wrapper'

>>> greet
<function decorated_return.<locals>.wrapper at 0x7f3fc574c550>
```

To preserve the information of function (as `greet` have changed to `wrapper`) we can use `@functools.wraps`.

```python
import functools

def decorated_return(func):
    functools.wraps(func)	# to preserve the info of func function
    def wrapper(*args, **kwargs):
        print("Custom Wrapper Script")
        return "Hi! " + func(*args, **kwargs)
    return wrapper

@decorated_return
def greet(name):
    return name.title()

print(greet('HP'))
```

Now we have info about the function passed to decorators and not the decorator itself.

```python
>>> greet.__name__
'greet'
>>> greet
<function greet at 0x7f6fb114de50>
```

## Custom Decorator Boilerplate

```python
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator
```
