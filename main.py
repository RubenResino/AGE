import common
import init, selection, crossing, mut, evaluation,fakeeval
import time, numpy as np, random

POPULATION = None
POP_LEN = 50
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
ARG_ALG_CROSSRATIO = 100

print(">>> INITIALIZING POP.")
#Initializes popuplation
POPULATION = init.initPopulation(POP_LEN)
print(POPULATION[0])
#POP_LEN = len(POPULATION)
print("<<< POP. INITIALIZED - SIZE:", POP_LEN)

# DOGEN
for i in range(ARG_ALG_ITERS):
    INTERMEDIATE = []
    print("Iteracion: ",i)

    print("popLen: ", len(POPULATION))
    print(">>> EVALUATING INDIVIDUALS")
		#Sets the fitness of the population

    start = time.time()
    for i, individual in enumerate(POPULATION):
        individual.fitness = evaluation.evaluate(individual)
    	print("<<< ", i)
    print("popLen: ", len(POPULATION))
    print("Primera evaluacion: ",time.time()-start)
    print("Maximo y media: ", common.maxmeanFit(POPULATION))

    while len(INTERMEDIATE) < POP_LEN:



        start = time.time()

		# Sorts population list
        POPULATION.sort(key = lambda x: x.fitness, reverse = False)
		# Populates intermediate list with best individuals
        best_fitness = POPULATION[0].fitness
        limit_fitness = best_fitness - (best_fitness * ARG_ALG_RANGERATIO)
        print("Ordenacion: ",time.time()-start)

        start = time.time()

        for individual in range(ARG_ALG_BESTPICKS):
			# If individual fitness is greater than the specified range, stop loop
            if POPULATION[individual].fitness < limit_fitness:
                break

			# Push individual to intermediate list
            INTERMEDIATE.append(POPULATION[individual])

        print("Mantener padres: ",time.time()-start)
        start = time.time()

    	# Choses between mutation or crossing
        if random.randint(0, 100) < ARG_ALG_CROSSRATIO:
            print(">>> SELECTING INDIVIDUAL")
            parents = (selection.tournament(POPULATION, ARG_SEL_TSIZE), selection.tournament(POPULATION, ARG_SEL_TSIZE))
            print(">>> CROSSING INDIVIDUAL")
            print("Aqui")
            for child in crossing.love(parents, ARG_CRS_SWAPS):

                # Creates a Chromo object to pass to the new population
                newIndiv = common.Chromo(child)
                INTERMEDIATE.append(newIndiv)
            print("final")
        else:
            newIndiv = common.Chromo(mut.mutation(selection.tournament(POPULATION, ARG_SEL_TSIZE)))
            INTERMEDIATE.append(newIndiv)
        print("Generacion individuos: ",time.time()-start)

    POPULATION = INTERMEDIATE
