# Class Methods

Result of execution of [Class Method Decorators](class_static_property.py)

## Code

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        """Get value of radius"""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Set radius, raise error if negative"""
        if value >= 0:
            self._radius = value
        else:
            raise ValueError("Radius must be positive")

    @property
    def area(self):
        """Calculate area inside circle"""
        return self.pi() * self.radius**2

    def cylinder_volume(self, height):
        """Calculate volume of cylinder with circle as base"""
        return self.area * height

    @classmethod
    def unit_circle(cls):
        """Factory method creating a circle with radius 1"""
        return cls(1)

    @staticmethod
    def pi():
        """Value of π, could use math.pi instead though"""
        return 3.1415926535
```

## Execution

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

`.cylinder_volume()` is a regular method.

`.radius` is a mutable property: it can be set to a different value. However, by defining a setter method, we can do some error testing to make sure it’s not set to a nonsensical negative number. Properties are accessed 
as attributes without parentheses.

`.area` is an immutable property: properties without `.setter()` methods can’t be changed. Even though it is defined as a method, it can be retrieved as an attribute without parentheses.

`.unit_circle()` is a class method. It’s not bound to one particular instance of Circle. Class methods are often used as factory methods that can create specific instances of the class.

`.pi()` is a static method. It’s not really dependent on the Circle class, except that it is part of its namespace. Static methods can be called on either an instance or the class.
