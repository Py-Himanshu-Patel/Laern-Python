# Singleton Pattern

**Classification**: Creational
This pattern is used for creation of object. Infact Singleton enfore that class must have only one object. This provide global poiint of access. Also class is reponsible for its one intance. Also provide **lazy** instantiation is object is costly to instantiate or less likely to use.

`object.__dict__`  
A dictionary or other mapping object used to store an object’s (writable) attributes.

`object.__call__(self[, args...])`  
Called when the instance is **called** as a function; if this method is defined, `x(arg1, arg2, ...)` roughly translates to `type(x).__call__(x, arg1, ...)`.

## Simple Example

```python
class Singleton:
    ans = None

    @staticmethod
    def instance():
        if '_instance' not in Singleton.__dict__:
            Singleton._instance = Singleton()
        return Singleton._instance

s1 = Singleton.instance()
s2 = Singleton.instance()

assert s1 is s2

s1.ans = 10

assert s1.ans == s2.ans

print("Test Passed")
```

While using `@staticmethod` we dont pass `self` parameter to method.

## Classic Example : Logger

A more classic example is of Logger which need only one instance of class for execution and loggin all the required activities.

```python
import datetime

class Logger:
    log_file = None

    @staticmethod
    def instance():
        if '_instance' not in Logger.__dict__:
            Logger._instance = Logger()
        return Logger._instance

    def open_log(self, path):
        self.log_file = open(path, mode='w')
        self.log_file.writelines('\n')

    def write_log(self, log_record):
        now = str(datetime.datetime.now().strftime("%m-%d-%Y, %H:%M:%S"))
        record = f"{now}: {log_record}"
        self.log_file.writelines(record)
    
    def close_log(self):
        self.log_file.close()


logger = Logger()
logger.open_log('MyLog.log')
logger.write_log('Logger with classic Singleton pattern')
logger.close_log()

with open('MyLog.log', 'r') as log:
    for line in log:
        print(line)
```

Singleton is called **antipattern** because some of the cons.

- **Violates Single Responsiblity Priciple**: Same logger class is making a file connection and maintaining it.

- **Non-Standard class access**: To get instance we must know the class is singleton and then use `_instance` method to get already instantiated object.

- **Testing**: They make unit testing very hard. They introduce global state to the application. The problem is that you cannot completely isolate classes dependent on singletons. Difficult to make mockups.

## Base Class Example : Fix Single Responsiblity Problem

Building a base class for all singleton.

Whenever a class is instantiated `__new__` and `__init__` methods are called. `__new__` method will be called when an object is created and `__init__` method will be called to initialize the object.

```python
class class_name:
    def __new__(cls, *args, **kwargs):
        statements
        .
        .
        return super(class_name, cls).__new__(cls, *args, **kwargs)
```

```python
class MyClass:
    def __new__(cls):
        print("Making new object")
        return super(MyClass, cls).__new__(cls)

    def __init__(self):
        print("Initializing new object")

obj = MyClass()
print('-- obj created --')

# Making new object
# Initializing new object
# -- obj created --
```

### Logger with Base Singleton class

```python
import datetime

class Singleton:
    _instances = {}		# dict([cls, instance])

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance
        return cls._instances[cls]

# from Singleton_BaseClass import Singleton

class Logger(Singleton):
    log_file = None

    # need for open file method is removed
    def __init__(self, path):
        if not self.log_file:
            self.log_file = open(path, 'w')
    
    def write_log(self, log_record):
        now = datetime.datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
        record = f"{now}: {log_record}"
        self.log_file.writelines(record + "\n")

    def close_log(self):
        if self.log_file:
            self.log_file.close()
            self.log_file = None

# need for Logger.instance() is removed
logger1 = Logger('MyLog2.log')
logger1.write_log('First Line of log')
logger2 = Logger('SameLogFile.log')
logger2.write_log('Second Line of log')
logger1.close_log()
logger2.close_log()


with open('MyLog2.log', 'r') as log:
    for line in log:
        print(line)
```

In `MyLog2.log`. Notice `SameLogFile.log` is not even created as long as first object of Logger is present.

```text
06-01-2021, 10:20:20: First Line of log
06-01-2021, 10:20:20: Second Line of log
```
