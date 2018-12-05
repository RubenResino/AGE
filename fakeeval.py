import random

def evaluate(chromo):
  chromo.fitness = random.uniform(0, 1) * random.randint(0, 100)
