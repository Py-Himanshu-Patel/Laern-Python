from abc import ABC, abstractmethod

class Switchable(ABC):
	@abstractmethod
	def turn_on(self):
		pass
	
	@abstractmethod
	def turn_off(self):
		pass

# we can't instantiate an abstract class neither 
# any other class which inherit abstract class and 
# do not implement even one of its abstractmethod 

# s = Switchable()


class LightBulb(Switchable):
	def turn_on(self):
		print('LightBulb: turned on')

	def turn_off(self):
		print('LightBulb: turned off')


class Fan(Switchable):
	def turn_on(self):
		print('Fan: turn on')

	def turn_off(self):
		print('Fan: turn off')


class ElectricPowerSwitch:
	def __init__(self, c: Switchable):
		self.client = c
		self.on = False

	def press(self):
		if self.on:
			self.client.turn_off()
			self.on = False
		else:
			self.client.turn_on()
			self.on = True

f = Fan()
switch = ElectricPowerSwitch(f)
switch.press()
switch.press()
