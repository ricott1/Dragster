import random
import brain


class Runner(object):
	def __init__(self, index, pool, generation, max_energy, structure):
		self.index = index
		self.pool = pool
		self.generation = generation
		self.id = str(self.pool)
		self.max_energy = max_energy
		self.energy = self.max_energy

		self.velocity = 0
		self.position = 0
		self.output = 0
		self.isArrived = 0

		self.brain = brain.Brain(structure)

	def update(self, inputs):
		self.output = self.brain.propagate(inputs, 0)[0]
		self.position += self.velocity
		
		if self.energy  - (self.velocity + self.output) > 0:
			self.velocity = max(0, min(self.max_energy, self.velocity + self.output))
			self.energy = min(self.max_energy, self.energy - self.velocity)
		elif self.energy  - self.velocity > 0:
			self.velocity = max(0, min(self.max_energy, self.velocity))
			self.energy = min(self.max_energy, self.energy - self.velocity)
		else:
			self.max_energy = max(0, self.max_energy - 0.01)
			self.velocity = max(0, min(self.max_energy, self.velocity))
			self.energy = min(self.max_energy, max(0, self.energy + 0.01))

	def recover(self, j):
		bonus = max(0, 0.0005 * (10 - j))
		self.max_energy = min(1, self.max_energy + bonus)

	def print_state(self):
		return "{:5s}: x = {:6.2f}; v = {:.2f}; e = {:4.2f}/{:4.2f}".format(self.id[-5:], f(self.position), f(self.velocity), f(self.energy), f(self.max_energy) )



def f(value):
	return round(value, 2)


