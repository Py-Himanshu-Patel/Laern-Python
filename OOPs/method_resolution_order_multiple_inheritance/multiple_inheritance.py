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
