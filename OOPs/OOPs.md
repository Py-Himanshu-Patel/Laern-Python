# Object Oriented Programming

## Key Points

- Using `is` returns True only for objects that are the exact same instance.
- A singleton is a class with only one instance.

## Class Methods

Result of execution of [Class Method Decorators](class_method_decorators.py)

```python
# creating circle
>>> c = Circle(5)
>>> c
<__main__.Circle object at 0x7fed37f3ad60>
>>> c.radius
5

# getting area as function and then as attribute
>>> c.area()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'float' object is not callable
>>> c.area
78.5398163375

# setting radius and area
>>> c.radius = 1
>>> c.area
3.1415926535
>>> c.radius = -2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 14, in radius
ValueError: Radius must be positive
>>> c.area = 100
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: cant set attribute

# checking usual object method
>>> c.cylinder_volume(4)
12.566370614

# check if static method is available globally
>>> pi()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'pi' is not defined

# static method is available from obj and class
>>> c.pi()
3.1415926535
>>> Circle.pi()
3.1415926535

# class method can be called using class without making obj
>>> Circle.unit_circle()
<__main__.Circle object at 0x7fed37ebe340>
>>> Circle.unit_circle().radius
1

```
