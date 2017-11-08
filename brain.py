import math, random


class Brain(object):
  """Initialize the Brain. Structure is a list with the hidden neurons tructure. Ex: structure = [6, 2, 4] if there are 6 inputs."""
  def __init__(self, structure):
    self.structure = structure
    self.coefficients = initialize_coeffs(structure, 0, 1)
    self.intercepts = initialize_intercepts(structure, 0, 1)
    self.f = relu

  def propagate(self, inputs, layer):
    M = transpose(self.coefficients[layer])
    b = self.intercepts[layer]
    outputs = [self.output(M[i], inputs, b[i]) for i in xrange(len(b))]
    if layer < len(self.coefficients) - 1:
      outputs = self.propagate(outputs, layer + 1)
    return outputs

  def output (self, w, x, c):
    out = c + sum([w[i] * x[i] for i in xrange(len(x))])
    return self.f(out)

  def mutate(self, mutation_rate):
    self.intercepts = [[self.intercepts[i-1][j] + 2 * (random.random() - 0.5) * mutation_rate for j in xrange(self.structure[i])] for i in xrange(1, len(self.structure))]
    self.coefficients = [[[self.coefficients[i][j][k] + 2 * (random.random() - 0.5) * mutation_rate for k in xrange(self.structure[i+1])] for j in xrange(self.structure[i])] for i in xrange(len(self.structure)-1)]

def initialize_intercepts(structure, mean, variance):
  intercepts = [[mean + 2 * (random.random() - 0.5) * variance for j in xrange(structure[i])] for i in xrange(1, len(structure))]
  return intercepts


def initialize_coeffs(structure, mean, variance):
   coeffs = [[[mean + 2 * (random.random() - 0.5) * variance for k in xrange(structure[i+1])] for j in xrange(structure[i])] for i in xrange(len(structure)-1)]
   return coeffs



def rescale(inputs, means, scales):
   return [(inputs[i] - means[i]) / scales[i] for i in xrange(len(inputs))]

def transpose(M):
  return zip(*M)

def relu(x):
  return max(0, x)

def identity(x):
  return x

def logistic(x):
  return 1.0 / (1 + math.exp(-x))

def tanh(x):
  return math.tanh(x)

