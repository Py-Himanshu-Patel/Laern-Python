# Factory Pattern

**Classification**: Creational  
This pattern define an interface for subclass to create an object. But it lets subclass decide which object to create. It is also know as virtual constructor pattern.

First we make a `Abstract Base Class` and then make concrete classes based on this only.

```python
# abstract_auto.py
from abc import ABC, abstractmethod


class AbstractAuto(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
```

```python
# implement all concrete class whome we want to instantiate

from .abstract_auto import AbstractAuto


class Duster(AbstractAuto):
    def start(self):
        print("Duster started")

    def stop(self):
        print("Duster stopped")

class Kia(AbstractAuto):
    def start(self):
        print("Kia started")

    def stop(self):
        print("Kia stopped")


class Nano(AbstractAuto):
    def start(self):
        print("Nano started")

    def stop(self):
        print("Nano stopped")

class Nexon(AbstractAuto):
    def start(self):
        print("Nexon started")

    def stop(self):
        print("Nexon stopped")


class NullCar(AbstractAuto):
    def __init__(self, carname):
        self._carname = carname

    def start(self):
        print('Unknown car "%s".' % self._carname)

    def stop(self):
        pass
```

To access all the class we declared here in `autos` package we need to bring all those classes to `__init__.py` file as this is the only file which gets loaded into module which calls `import autos`. Also notice the way we called adjacent files using a period `.` before the name of file. This is not done when we import the neighbout module as library for instantiation.

```python
from .duster import Duster
from .nano import Nano
from .kia import Kia
from .nexon import Nexon
from .abstract_auto import AbstractAuto
```

Now is the time when we make a factory which takes a class name as string and return its object. To do this we basically make a mapping for each classname and its class. When called with a name as string we return corresponding classes object.

```python
from inspect import isclass, isabstract, getmembers
import autos


def isconcrete(obj):
    return isclass(obj) and not isabstract(obj)


class AutoFactory:
    vehicles = {}      # { car model name: class for the car}

    def __init__(self):
        self.load_autos()

    def load_autos(self):
        classes = getmembers(autos, isconcrete)

        for name, _type in classes:
            if isclass(_type) and issubclass(_type, autos.AbstractAuto):
                self.vehicles.update([[name, _type]])

    def create_instance(self, carname):
        if carname in self.vehicles:
            return self.vehicles[carname]()
        return autos.NullCar(carname)
```

Python main file for execution.

```python
from autoFactory import AutoFactory

factory = AutoFactory()

for carname in ['Nano', 'Nexon', 'Kia', 'Duster']:
    car = factory.create_instance(carname)
    car.start()
    car.stop()
```
