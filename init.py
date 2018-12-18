import random
import common

from random import randint

#Index of the nodes of the tree
element_ = 0
depth_ = 1
son_ = 2
written_ = 3

both_ = 2

# Gets a node and return it if it not cte. Otherwise, it returns a random float
def getRandomCte(element):
	return str(round(random.uniform(0.1,10),3)) if (element is 'cte') else element

#Create a node of the tree according to the type
def createNode(mode, currentDepth):
	newNode=[getRandomCte(common.getSymbol(mode)),currentDepth,[],"no"]
	if common.determineNode(newNode[element_]) is common.terminal_:
		newNode[son_].append(-1)
	return newNode

#Determines the type of the node which will be created
def determineMode(currentDepth, maxDepth, mode):
	if(currentDepth==maxDepth-1): #Max depth will always be a terminal
		return common.terminal_
	else: #In other case
		if(mode=='full'): #If full all nodes will be functions
			return common.function_
		elif (mode=='grow'): #If grow all nodes less dept 0 and max-1 will be selected randomly
			return both_

#Create the sons of the nodes
def addSons(indiv, currentDepth, maxDepth, mode):
	for node in indiv: #Go trhought all the nodes of the tree
		if(node[depth_]==currentDepth-1): #Check if the node is a posible parent for the current depth, this is, the current depth minus one
			if common.determineNode(node[element_]) is common.function_: #Check if the node is a function, this is, it can have sons
				for x in range(common.getArity(node[element_])): #We execute this as many times as children can have the element
					#Create the a son
					indiv.append(createNode(determineMode(currentDepth, maxDepth, mode),currentDepth))
					#Add sons to the parent list of sons
					node[son_].append(len(indiv)-1)
	return indiv

def initIndiv(maxDepth,mode):
	#List of list: the 2nds will be: [element, depth, [sons], written]
	#The sons sublist will give the index of the son on the indiv list
	#Terminals will have a -1 as child to indicate they dont have children
    indiv = []

    #########ERROR CHECKS
    #If < 0 returns an error
    if(maxDepth<0):
    	print("Error: negative depth")
    	return

    #If 0 returns an empty list
    if(maxDepth==0):
    	print("Warning: empty individual")
    	return indiv

    #If 1 returns a terminal
    if(maxDepth==1):
    	return [getRandomCte(common.getSymbol(common.terminal_))]

    ##########TREE CREATION
    for currentDepth in range(maxDepth):
        if (currentDepth==0): #Root node will be a function
            indiv.append(createNode(common.function_,currentDepth))
        else:
        	indiv=addSons(indiv, currentDepth, maxDepth, mode)

    #To store the final chromosoma
    newIndiv = []
    #List of openList nodes
    openList = [indiv[0]]

    ########TRANSLATION FROM TREE TO CHROMO
    while len(openList)!=0:

    	if (openList[-1][written_] is "no"):
    		#We add its element just if we did not add it before.
    		#This is cause we can get several times the same element as the last one of the openList list
    		newIndiv.append(openList[-1][element_])
    		openList[-1][written_]="yes"

    	numSons=len(openList[-1][son_])
    	noneSons = 0

    	for y in range(numSons):
    		if openList[-1][son_][y] is -1:
    			#If the son is -1 (this is, a terminal son or a function son which have already been studied), we discard it
    			noneSons+=1
    		else:
    			#Son not studied: add it to openList list and put it as studied. Break of the loop cause we have get one.
    			openList.append(indiv[openList[-1][son_][y]])
    			openList[-2][son_][y]=-1
    			break
    	if (numSons==noneSons):
    		#If all sons -1 (terminal or all function's sons studied) we close the node
    		openList.pop()
    return newIndiv

#Till the pop is full
def initPopulation(popSize,growProb,maxDepth):
	#Generate the whole population
	population=[]

	while(popSize>0):
		#We generate a random number of indivs with the same configuration
		#If we have left more than 10 indivs the maximum will be the number of indivs_left/ 2
		if(popSize>10):
			elems=int(popSize/2)
		#If we have less the maximum will be the indivs left
		else:best_individual
			elems=popSize

		numIndivs=randint(0,elems)
		popSize-=numIndivs

		#Determine a configuration
		depth=randint(2,maxDepth)

		if(random.random()<growProb):
			mode = "grow"
		else:
			mode="full"

		#Create num_indivs with the given configuration
		while (numIndivs!=0):
			chromoIndiv=common.Chromo()
			chromoIndiv.allels=initIndiv(depth,mode)
			population.append(chromoIndiv)
			numIndivs-=1
	return population

"""
pop=initPopulation(50)
for i in range(len(pop)):
	print(pop[i].allels)
"""
