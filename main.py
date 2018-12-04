import common
import evaluation, init, selection, crossing, mut
import time, numpy as np, random

POPULATION = None
POP_LEN = 2
INTERMEDIATE = None

"""
    Algortihm arguments
"""
ARG_SEL_TSIZE = 3           				# Selection; tournament size
ARG_CRS_SWAPS = 2           				# Crossing; number of chromosome swaps in each crossing
ARG_ALG_ITERS = 50          				# Iterations through algorithm
ARG_ALG_tFEED = 10          				# When to print feedback
ARG_ALG_RANGERATIO = 5						# Percent. Min fitness range difference between the best individual and the individuals chosen for the new population
ARG_ALG_BESTPICKS = int(POP_LEN * 0.2)		# Top limit of individuals selected for the new population
ARG_ALG_CROSSRATIO = 70

print(">>> INITIALIZING POP.")
#Initializes popuplation
POPULATION = init.initPopulation(POP_LEN)
#POP_LEN = len(POPULATION)
print("<<< POP. INITIALIZED - SIZE:", POP_LEN)

# DOGEN
for i in range(ARG_ALG_ITERS):
    INTERMEDIATE = []

    while len(INTERMEDIATE) < POP_LEN:

        print("popLen: ", len(POPULATION))
        print(">>> EVALUATING INDIVIDUALS")
		#Sets the fitness of the population
        for i, individual in enumerate(POPULATION):
            evaluation.evaluate(individual)
            print("<<< ", i)
        print("popLen: ", len(POPULATION))


		# Sorts population list
        POPULATION.sort(key = lambda x: x.fitness, reverse = False)
		# Populates intermediate list with best individuals
        best_fitness = POPULATION[0].fitness
        limit_fitness = best_fitness - (best_fitness * ARG_ALG_RANGERATIO)

        for individual in range(ARG_ALG_BESTPICKS):
			# If individual fitness is greater than the specified range, stop loop
            if POPULATION[individual].fitness < limit_fitness:
                break

			# Push individual to intermediate list
            INTERMEDIATE.append(POPULATION[individual])

    	# Choses between mutation or crossing
        if random.randint(0, 100) < ARG_ALG_CROSSRATIO:
            print(">>> SELECTING INDIVIDUAL")
            parents = (selection.tournament(POPULATION, ARG_SEL_TSIZE), selection.tournament(POPULATION, ARG_SEL_TSIZE))
            print(">>> CROSSING INDIVIDUAL")
            print("Aqui")
            for child in crossing.love(parents, ARG_CRS_SWAPS):
                INTERMEDIATE.append(child)
            print("final")
        else:
            INTERMEDIATE.append(mut.mutation(selection.tournament(POPULATION, ARG_SEL_TSIZE)))

    POPULATION = INTERMEDIATE
