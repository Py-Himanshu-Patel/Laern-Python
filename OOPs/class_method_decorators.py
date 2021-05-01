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

"""
.cylinder_volume() is a regular method.

.radius is a mutable property: it can be set to a different value. 
However, by defining a setter method, we can do some error testing to make 
sure it’s not set to a nonsensical negative number. Properties are accessed 
as attributes without parentheses.

.area is an immutable property: properties without .setter() methods can’t be 
changed. Even though it is defined as a method, it can be retrieved as an attribute 
without parentheses.

.unit_circle() is a class method. It’s not bound to one particular instance of Circle. 
Class methods are often used as factory methods that can create specific instances 
of the class.

.pi() is a static method. It’s not really dependent on the Circle class, except that 
it is part of its namespace. Static methods can be called on either an instance or 
the class.
"""