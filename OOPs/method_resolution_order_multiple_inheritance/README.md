# Multiple Inheritance and MRO (Method Resolution Order)

## With Over Riding Method

```python
class Father:
    def __init__(self) -> None:
        print("Father Const")

class Mother:
    def __init__(self) -> None:
        print("Mother Const")

class Son(Father, Mother):
    def __init__(self) -> None:
        print("Son Const")

# ------------------------------

s = Son()
```

Output

```bash
Son Const
```

When **Child** class overrides the method of its **Parent** class then only the method of child class is called.

But what if **Child** class do not override the constructor of its **Parent** class.

## Without Over Riding Method

```python
class Father:
    def __init__(self) -> None:
        print("Father Const")

class Mother:
    def __init__(self) -> None:
        print("Mother Const")

class Son(Father, Mother):
    pass
# ------------------------------

s = Son()
```

Output

```bash
Father Const
```

When child class do not override the method then the MRO specify the **left to right traversal** on parent method (in sequence of inheritance) using depth first search.

What if Mother is inherited first.

```python
class Father:
    def __init__(self) -> None:
        print("Father Const")

class Mother:
    def __init__(self) -> None:
        print("Mother Const")

class Son(Mother, Father):
    pass
# ------------------------------

s = Son()
```

Output

```bash
Mother Const
```

Same is the result if we do

```python
class Son(Father, Mother):
    def __init__(self) -> None:
        super().__init__()
```

OR

```python
class Son(Mother, Father):
    def __init__(self) -> None:
        super().__init__()
```

Till here we are happy if we want only one 

But now lets see how **depth first search** effect this. Also we want **output of both** the overridden method.

## Call super() - DFS and left to right traversal

```python
class Father:
    def __init__(self) -> None:
        super().__init__()
        print("Father Const")

class Mother:
    def __init__(self) -> None:
        super().__init__()
        print("Mother Const")

class Son(Father, Mother):
    def __init__(self) -> None:
        super().__init__()
        print("Son Const")

# ------------------------------

s = Son()
```

Output

```bash
Mother Const
Father Const
Son Const
```

```bash
Son ---> Father ---> Object (init)
                       |
                       v
Son <--- Father <--- Mother
(init)   (init)     (init)
```

First starting from `Son` access the `Father` class then `Father` class access it's parent class which is `Object` and since the `Object` class do not have any parent thus it's `__init__` method gets executed and it further looks for other class in multiple inheritance of `Son` class and visit them (in DFS manner) here it is `Mother` class. Then we trackback and visit `Father` and `Son` class.

What if we change the order of inheritance.

```python
class Father:
    def __init__(self) -> None:
        super().__init__()
        print("Father Const")

class Mother:
    def __init__(self) -> None:
        super().__init__()
        print("Mother Const")

class Son(Mother, Father):
    def __init__(self) -> None:
        super().__init__()
        print("Son Const")

# ------------------------------

s = Son()
```

Output

```bash
Father Const
Mother Const
Son Const 
```

```bash
Son ---> Mother ---> Object (init)
                       |
                       v
Son <--- Mother <--- Father
(init)   (init)     (init)
```

## Method which are not constructor - DFS do not go till object class

```python
class Father:
    def method(self) -> None:
        print("Father Method")

class Mother:
    def method(self) -> None:
        print("Mother Method")

class Son(Father, Mother):
    def method(self) -> None:
        super().method()
        print("Son Method")

class Daughter(Mother, Father):
    def method(self) -> None:
        super().method()
        print("Son Method")

# ------------------------------

s = Son()
s.method()

print('-----------')

d = Daughter().
d.method()
```

Output

```bash
Father Method
Son Method
-----------
Mother Method
Son Method
```

Observe only one method gets called that too from first class (in sequence of inheriting) which provid that method.

## Method which are not constructor - DFS go till object class

```python
class GrandParent(object):
    def method(self):
        print("Grand Parent")

class Father(GrandParent):
    def method(self) -> None:
        super().method()
        print("Father Method")

class Mother(GrandParent):
    def method(self) -> None:
        super().method()
        print("Mother Method")

class Son(Father, Mother):
    def method(self) -> None:
        super().method()
        print("Son Method")

class Daughter(Mother, Father):
    def method(self) -> None:
        super().method()
        print("Son Method")

# ------------------------------

s = Son()
s.method()

print('-----------')

d = Daughter()
d.method()
```

Output

```bash
Grand Parent
Mother Method
Father Method
Son Method   
-----------  
Grand Parent 
Father Method
Mother Method
Son Method
```
