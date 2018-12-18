import common
import copy
import init, selection, crossing, mut, evaluation,fakeeval
import time, numpy as np, random, threading

POPULATION = None
POP_LEN = 50
INTERMEDIATE = None

"""
    Algortihm arguments
"""
METH_selectionTournament = getattr(selection, "tournament")
METH_selectionRoulette = getattr(selection, "RouletteMethod")

ARG_tournamentSize = 3           				# Selection; tournament size
ARG_selectivePressure = 1                       # Selection; selective pressure
ARG_crossingSwaps = 2           				# Crossing; number of chromosome swaps in each crossing
ARG_iterations = 50             				# Iterations through algorithm
ARG_itersPerFeedback = 10          				# When to print feedback
ARG_goodFitnessRatio = 5						# Percent. Min fitness range difference between the best individual and the individuals chosen for the new population
ARG_maxIndividualsKept = int(POP_LEN * 0.2)		# Top limit of individuals selected for the new population
ARG_crossingRatio = 0.7                         # Percent. Probability of picking crossing against mutation on each iteration
ARG_mutationTreeDepth = 3                       # Max depth of the tree generated in mutation
METH_selectingMethod = METH_selectionTournament # Selecting method using during population generation.
ARG_selectingMethodParam = ARG_tournamentSize   # if tournament, param is tournament size, if roulette, param is selective pressure
"""
    Multithreading
"""
MT_T_NUMB = 4   # Number of threads

# Generic method to run some chunk of data in some other method
# This is used when slicing a loop with multithreading
# "data" is a list of elements that the called method must iterate through
def task_slice(data, method):
    method(data)

# Generic method to fire a method either using threading or not
# "data" is a list of elements that the called method must iterate through
def task_fire(data, method, using_threading):
    # Threading disabled. Runs method as usual
    if not using_threading:
        method(data)

    # Enables threading capabilities
    else:
        # Where threads will be stored
        t_list = []

        # Splits task in available threads. Data should be splitted too
        for t in range(MT_T_NUMB):
            i_split = t * MT_T_NUMB

            # Splitted data list
            t_data = data[i_split : (i_split + int(len(data) / MT_T_NUMB) + 1)]

            # Creates thread. target is the method to run, args are its arguments...
            thread = threading.Thread(target = task_slice, args = (t_data, method))

            # Starts and appends thread to thread list
            thread.start()
            t_list.append(thread)

        # Once every thread has been initialized, we'll check its number
        #print("Active threads: ", str(threading.activeCount()))

        # Waits for threads to finish
        for t in t_list:
            t.join()
        #print("Task is over")

        # Empties thread list
        t_list = []


# Dummy evaluation method. Evaluates a whole population.
# This should be defined elsewhere...
def evaluate_bulk(population):
    for i, individual in enumerate(population):
        individual.fitness = evaluation.evaluate(individual)
        #print("<<< ", i)




# print(">>> INITIALIZING POP.")
# Initializes popuplation
POPULATION = init.initPopulation(POP_LEN)
# print(POPULATION[0])
#POP_LEN = len(POPULATION)
# print("<<< POP. INITIALIZED - SIZE:", POP_LEN)

# DOGEN
for i in range(ARG_iterations):
    INTERMEDIATE = []
    print("Iteracion: ",i)

    # print("popLen: ", len(POPULATION))
    # print(">>> EVALUATING INDIVIDUALS")
		#Sets the fitness of the population

    # start = time.time()
    """
    for i, individual in enumerate(POPULATION):
        individual.fitness = fakeeval.evaluate(individual)
        print("<<< ", i)
    """

    # Evaluation
    # When threading is enabled, evaluation across population is asynchronous
    #task_fire(POPULATION, evaluate_bulk, True)
    evaluate_bulk(POPULATION)


	# Sorts population list
    POPULATION.sort(key = lambda x: x.fitness, reverse = True)
    common.maxmeanFit(POPULATION)
    print(POPULATION[0].allels)
	# Populates intermediate list with best individuals
    best_fitness = POPULATION[0].fitness
    limit_fitness = best_fitness - abs(best_fitness * ARG_goodFitnessRatio)



    for individual in range(ARG_maxIndividualsKept):
		# If individual fitness is greater than the specified range, stop loop
        if POPULATION[individual].fitness < limit_fitness:
            break

		# Push individual to intermediate list
        INTERMEDIATE.append(copy.deepcopy(POPULATION[individual]))




    # print("popLen: ", len(POPULATION))
    # print("Primera evaluacion: ",time.time()-start)
    # print("Maximo y media: ", common.maxmeanFit(POPULATION))

    while len(INTERMEDIATE) < POP_LEN:

        #If there is only one element left we force the mutations
        if (len(INTERMEDIATE)==POP_LEN-1):
        	prob=0.8
        else:
        	prob=random.random()

    	# Choses between mutation or crossing
        if  prob < ARG_crossingRatio:
            # print(">>> SELECTING INDIVIDUAL")
            parents = (METH_selectingMethod(POPULATION, ARG_selectingMethodParam), METH_selectingMethod(POPULATION, ARG_selectingMethodParam))
            # print(">>> CROSSING INDIVIDUAL")
            for child in crossing.love(parents, ARG_crossingSwaps):

                # Creates a Chromo object to pass to the new population
                newIndiv = common.Chromo(child)
                INTERMEDIATE.append(newIndiv)

        else:
            newIndiv = common.Chromo(mut.mutation(METH_selectingMethod(POPULATION, ARG_selectingMethodParam), ARG_mutationTreeDepth))
            INTERMEDIATE.append(newIndiv)
        #print("Generacion individuos: ",time.time()-start)

    POPULATION = INTERMEDIATE
