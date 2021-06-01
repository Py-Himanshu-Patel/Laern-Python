# Builder Pattern

**Classification**: Creational  
This pattern is used for creation of object. The intent of the Builder design pattern is to separate the construction of a complex object from its representation. By doing so, the same construction process can create different representations.  

The Builder design pattern solves problems like:

- How can a class (the same construction process) create different representations of a complex object?
- How can a class that includes creating a complex object be simplified?

## Regular Class

Build a class for construction of computer.

```python
# computer_regular.py

class Computer(object):

    def __init__(self, case, mainboard, cpu, memory, hard_drive, video_card):
        self.case = case
        self.mainboard = mainboard
        self.cpu = cpu
        self.memory = memory
        self.hard_drive = hard_drive
        self.video_card = video_card

    def display(self):
        print('Custom Computer:')
        print('\t{:>10}: {}'.format('Case', self.case))
        print('\t{:>10}: {}'.format('Mainboard', self.mainboard))
        print('\t{:>10}: {}'.format('CPU', self.cpu))
        print('\t{:>10}: {}'.format('Memory', self.memory))
        print('\t{:>10}: {}'.format('Hard drive', self.hard_drive))
        print('\t{:>10}: {}'.format('Video card', self.video_card))

# in main.py
# from computer_regular import  Computer

computer = Computer(case='Coolermaster N300',
                    mainboard='MSI 970',
                    cpu='Intel Core i7-4770',
                    memory='Corsair Vengeance 16GB',
                    hard_drive='Seagate 2TB',
                    video_card='GeForce GTX 1070'
                    )

computer.display()
```

```bash
Custom Computer:
              Case: Coolermaster N300
         Mainboard: MSI 970
               CPU: Intel Core i7-4770
            Memory: Corsair Vengeance 16GB
        Hard drive: Seagate 2TB
        Video card: GeForce GTX 1070
```

This method have following problem. (Client is one who utilize the class)

- Long list of parameters need to be passed to make object.
- Class attributes must be encapsulated and not exposed for client/user to set.
- Ordering of attribute set. We can't connect a hard drive before mother board.

## Solve exposed attributes for client to setup

This solved the problem of long list of parameter the client have to pass.

```python
class Computer:

    def display(self):
        print('Custom Computer:')
        print('\t{:>10}: {}'.format('Case', self.case))
        print('\t{:>10}: {}'.format('Mainboard', self.mainboard))
        print('\t{:>10}: {}'.format('CPU', self.cpu))
        print('\t{:>10}: {}'.format('Memory', self.memory))
        print('\t{:>10}: {}'.format('Hard drive', self.hard_drive))
        print('\t{:>10}: {}'.format('Video card', self.video_card))

# in main.py
# from computer_expose_attribute import Computer

class MyComputer:

    def get_computer(self):
        return self._computer

    def build_computer(self):
        computer = self._computer = Computer()
        computer.case = 'Coolermaster N300'
        computer.mainboard = 'MSI 970'
        computer.cpu = 'Intel Core i7-4770'
        computer.memory = 'Corsair Vengeance 16GB'
        computer.hard_drive = 'Seagate 2TB'
        computer.video_card = 'GeForce GTX 1070'

builder = MyComputer()
builder.build_computer()
computer = builder.get_computer()
computer.display()
```

This method have following problem.

- Class attributes must be encapsulated and not exposed for client/user to set.
- Ordering of attribute set. We can't connect a hard drive before mother-board.

## Encapsulate the the class (which bears the attribute) in another class

It solved problem of long parameter list client have to pass and also the problem where inside variables are exposed to client.

```python
class Computer:

    def display(self):
        print('Custom Computer:')
        print('\t{:>10}: {}'.format('Case', self.case))
        print('\t{:>10}: {}'.format('Mainboard', self.mainboard))
        print('\t{:>10}: {}'.format('CPU', self.cpu))
        print('\t{:>10}: {}'.format('Memory', self.memory))
        print('\t{:>10}: {}'.format('Hard drive', self.hard_drive))
        print('\t{:>10}: {}'.format('Video card', self.video_card))

# main.py
# from computer_encapsulate import Computer

class MyComputerBuilder(object):

    def get_computer(self):
        return self._computer

    def build_computer(self):
        self._computer = Computer()
        self._computer.case = 'Coolermaster N300'
        self._computer.mainboard = 'MSI 970'
        self._computer.cpu = 'Intel Core i7-4770'
        self._computer.memory = 'Corsair Vengeance 16GB'
        self._computer.hard_drive = 'Seagate 2TB'
        self._computer.video_card = 'GeForce GTX 1070'


builder = MyComputerBuilder()
builder.build_computer()
computer = builder.get_computer()
computer.display()
```

This method have following problem.

- Ordering of attribute set. We can't connect a hard drive before mother-board.

## Solving ordering problem by introducing class method

Class method gets called in order we want to add attribute.

```python
class Computer(object):

    def display(self):
        print('Custom Computer:')
        print('\t{:>10}: {}'.format('Case', self.case))
        print('\t{:>10}: {}'.format('Mainboard', self.mainboard))
        print('\t{:>10}: {}'.format('CPU', self.cpu))
        print('\t{:>10}: {}'.format('Memory', self.memory))
        print('\t{:>10}: {}'.format('Hard drive', self.hard_drive))
        print('\t{:>10}: {}'.format('Video card', self.video_card))

# from computer_ordering import Computer

class MyComputerBuilder(object):

    def get_computer(self):
        return self._computer

    def build_computer(self):
        self._computer = Computer()
        self.get_case()
        self.build_mainboard()
        self.install_mainboard()
        self.install_hard_drive()
        self.install_video_card()

    def get_case(self):
        self._computer.case = 'Coolermaster N300'
     
    def build_mainboard(self):
        self._computer.mainboard = 'MSI 970'
        self._computer.cpu = 'Intel Core i7-4770'
        self._computer.memory = 'Corsair Vengeance 16GB'

    def install_mainboard(self):
        pass

    def install_hard_drive(self):
        self._computer.hard_drive = 'Seagate 2TB'

    def install_video_card(self):
        self._computer.video_card = 'GeForce GTX 1070'


builder = MyComputerBuilder()
builder.build_computer()
computer = builder.get_computer()
computer.display()
```

This method have following problem.

- If we want a make a cheaper computer then we have to make another class same as `MyComputerBuilder` and we can modify the methods giving class a new name but the method like `build_computer` or `get_computer` or those which do not get modified remains same hence the code reduncency and update need to be done in all the classes which have been duplicated from this one.

## Real Builder Pattern

Three Parts

- **AbsBuilder**: It defines **BuildPart()** which specifies how many parts need to be implement.
- **ConcreteBuilder**: It implements the methods defined in **AbsBuilder**.
- **Director**: It calls the **GetResult** methods in right order to ensure ordering.

```python
# computer.py
class Computer:

    def display(self):
        print('Custom Computer:')
        print('\t{:>10}: {}'.format('Case', self.case))
        print('\t{:>10}: {}'.format('Mainboard', self.mainboard))
        print('\t{:>10}: {}'.format('CPU', self.cpu))
        print('\t{:>10}: {}'.format('Memory', self.memory))
        print('\t{:>10}: {}'.format('Hard drive', self.hard_drive))
        print('\t{:>10}: {}'.format('Video card', self.video_card))


# abstract_builder.py

# from computer import Computer
from abc import ABC, abstractmethod

class AbsBuilder(ABC):

    def new_computer(self):
        self._computer = Computer()

    def get_computer(self):
        return self._computer

    @abstractmethod
    def build_mainboard(self):
        pass

    @abstractmethod
    def get_case(self):
        pass

    @abstractmethod
    def build_mainboard(self):
        pass

    @abstractmethod
    def install_mainboard(self):
        pass

    @abstractmethod
    def install_hard_drive(self):
        pass

    @abstractmethod
    def install_video_card(self):
        pass

# desktop_builder.py

# from abstract_builder import AbsBuilder

class DesktopBuilder(AbsBuilder):

    def get_case(self):
        self._computer.case = 'Coolermaster N300'
     
    def build_mainboard(self):
        self._computer.mainboard = 'MSI 970'
        self._computer.cpu = 'Intel Core i7-4770'
        self._computer.memory = 'Corsair Vengeance 16GB'

    def install_mainboard(self):
        pass

    def install_hard_drive(self):
        self._computer.hard_drive = 'Seagate 2TB'

    def install_video_card(self):
        self._computer.video_card = 'GeForce GTX 1070'


# directory.py

class Director:

    def __init__(self, builder):
        self._builder = builder

    def build_computer(self):
        self._builder.new_computer()
        self._builder.get_case()
        self._builder.build_mainboard()
        self._builder.install_mainboard()
        self._builder.install_hard_drive()
        self._builder.install_video_card()

    def get_computer(self):
        return self._builder.get_computer()

# main.py

# from director import Director
# from desktop_builder import DesktopBuilder

computer_builder = Director(DesktopBuilder())
computer_builder.build_computer()
computer = computer_builder.get_computer()
computer.display()
```

Similarly if we want another product to be build then we can do it easily using another implementation for abstract method and hence remove code duplicacy.

```python
# laptop_builder.py

# from abstract_builder import AbsBuilder

class LaptopBuilder(AbsBuilder):

    def get_case(self):
        self._computer.case = 'IN WIN BP655'
     
    def build_mainboard(self):
        self._computer.mainboard = 'ASRock AM1H-ITX'
        self._computer.cpu = 'AMD Athlon 5150'
        self._computer.memory = 'Kingston ValueRAM 4GB'

    def install_mainboard(self):
        pass

    def install_hard_drive(self):
        self._computer.hard_drive = 'WD Blue 1TB'

    def install_video_card(self):
        self._computer.video_card = 'On board'


# main.py

# from director import Director
# from laptop_builder import LaptopBuilder

computer_builder = Director(LaptopBuilder())
computer_builder.build_computer()
computer = computer_builder.get_computer()
computer.display()
```
