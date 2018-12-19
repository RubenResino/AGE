import common
import copy
import init, selection, crossing, mut, evaluation,fakeeval
import time, numpy as np, random, threading, pandas as pd

POPULATION = None
POP_LEN = 30
INTERMEDIATE = None

"""
    Algortihm arguments
"""
METH_selectionTournament = getattr(selection, "tournament")
METH_selectionRoulette = getattr(selection, "RouletteMethod")

#Init arguments
ARG_initTreeLimitNodes = 100					# Init: limit number of nodes for the tree
ARG_initGrowProb = 0.5							# Init: probability of trees with mode grow
ARG_initTreeMaxDepth = 5						# Init: maximum depth of the trees

#Selection arguments
ARG_tournamentSize = 3           				# Selection; tournament size
ARG_selectivePressure = 1.5                     # Selection; selective pressure
ARG_selectingMethodParam = ARG_tournamentSize   # if tournament, param is tournament size, if roulette, param is selective pressure
METH_selectingMethod = METH_selectionTournament # Selecting method using during population generation.

#Crossing
ARG_crossingSwaps = 1           				# Crossing; number of chromosome swaps in each crossing
ARG_crossingBalace = True
ARG_crossingMaxDebalance = 3

#Mutation
ARG_notSimpleMut = 0.25
ARG_mutTreeLimitNodes = int(ARG_initTreeLimitNodes*0.3) #Mut: limit number for the subtrees generated
ARG_mutationTreeDepth = ARG_initTreeMaxDepth - 3                       		# Max depth of the tree generated in mutation

#Evaluation
ARG_maxIdleIters = 10                           # number of consecutive iterations the algorithm should run with the same best individual to stop

#Main
ARG_maxIndividualsKept = int(POP_LEN * 0.2)		# Top limit of individuals selected for the new population
ARG_goodFitnessRatio = 10						# Percent. Min fitness range difference between the best individual and the individuals chosen for the new population
ARG_crossingRatio = 0.8                         # Percent. Probability of picking crossing against mutation on each iteration


#Otros
ARG_itersPerFeedback = 1          				# When to print feedback
ARG_iterations = 50             				# Max iterations through algorithm


################################################################################################

ARG_selectionName = None

if METH_selectingMethod is METH_selectionTournament:
    ARG_selectionName = "tournament"

else:
    ARG_selectionName = "RouletteMethod"
"""
    Multithreading
"""

OUTPUT_test = "pSize"+str(POP_LEN)+"_iTLN"+str(ARG_initTreeLimitNodes)+"_mTLN"+str(ARG_mutTreeLimitNodes)+"_iGP"+str(ARG_initGrowProb)+"_iTMD"+str(ARG_initTreeMaxDepth)+"_tS"+str(ARG_tournamentSize)+"_sP"+str(ARG_selectivePressure)+"_cS"+str(ARG_crossingSwaps)+"_it"+str(ARG_iterations)+"_gFR"+str(ARG_goodFitnessRatio)+"_mIK"+str(ARG_maxIndividualsKept)+"_cR"+str(ARG_crossingRatio)+"_mTD"+str(ARG_mutationTreeDepth)+"_sM"+str(ARG_selectionName)+"_sMP"+str(ARG_selectingMethodParam)+"_mII"+str(ARG_maxIdleIters)

OUTPUT_results = []
columns = ["nombre", "mejor_fitness", "fitness_medio", "varianza_fitness"]
file = open(OUTPUT_test+".csv","w")
file_best = open("best_fun.txt", "w")
#df = pd.DataFrame(columns = columns)

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

##################################################################################################


# print(">>> INITIALIZING POP.")
# Initializes popuplation
POPULATION = init.initPopulation(POP_LEN,ARG_initGrowProb, ARG_initTreeMaxDepth, ARG_initTreeLimitNodes)
# print(POPULATION[0])
#POP_LEN = len(POPULATION)
# print("<<< POP. INITIALIZED - SIZE:", POP_LEN)

# DOGEN
# Number of iterations with same best individual
timesSameBest = 0
current_best = None
for i in range(ARG_iterations):
    #print("rawr")
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
    common.cleanPop(POPULATION)
    evaluate_bulk(POPULATION)


	# Sorts population list
    POPULATION.sort(key = lambda x: x.fitness, reverse = True)
    new_best = POPULATION[0]

    #df.append(pd.DataFrame(["HOLA",new_best.fitness, 0, 0],columns = columns),ignore_index=True)



    # Same best individual as in previous iteration
    if new_best is current_best:
        timesSameBest += 1

    # New best individual. Resets counter
    else:
        current_best = new_best
        timesSameBest = 0

    fit = common.maxmeanFit(POPULATION)

    #OUTPUT_test.append([str(i)+","+str(fit[0])+","+str(fit[1])+","])

    if i%ARG_itersPerFeedback == 0:
        file.write(str(i)+","+str(fit[0])+","+str(fit[1])+","+str(fit[2])+","+str(fit[3])+",\n")

    print("Best individual:")
    print(new_best.allels)
	# Populates intermediate list with best individuals
    best_fitness = new_best.fitness
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
    common.cleanPop(POPULATION)
    while len(INTERMEDIATE) < POP_LEN:

        #If there is only one element left we force the mutations
        if (len(INTERMEDIATE)==POP_LEN-1):
        	prob=ARG_crossingRatio+0.1
        else:
        	prob=random.random()

    	# Choses between mutation or crossing
        if  prob < ARG_crossingRatio:
            # print(">>> SELECTING INDIVIDUAL")
            parents = (METH_selectingMethod(POPULATION, ARG_selectingMethodParam), METH_selectingMethod(POPULATION, ARG_selectingMethodParam))
            # print(">>> CROSSING INDIVIDUAL")
            for child in crossing.love(parents, ARG_crossingSwaps, ARG_crossingBalace, ARG_crossingMaxDebalance):

                # Creates a Chromo object to pass to the new population
                newIndiv = common.Chromo(child)
                INTERMEDIATE.append(newIndiv)

        else:
            newIndiv = common.Chromo(mut.mutation(METH_selectingMethod(POPULATION, ARG_selectingMethodParam), ARG_mutationTreeDepth,ARG_mutTreeLimitNodes, ARG_notSimpleMut))
            INTERMEDIATE.append(newIndiv)
        #print("Generacion individuos: ",time.time()-start)

    POPULATION = INTERMEDIATE
file_best.write(str(current_best))
