import random
import math
import sys

# Structures of the common elements
# List of the whole population
#POPULATION = None

function_=0
terminal_=1

#Chromosoma structure
class Chromo:
    allels = []
    fitness = 0

    def __init__(self, allels = None):

        self.allels = []
        self.fitness = 0

        if allels is not None:
            self.allels = allels

# Common functions and methods
class Operator:
    arity = 0
    function = None

    def __init__(self, arity, function):
        self.arity = arity
        self.function = function

    def __call__(self, *args):
        assert(len(args) == self.arity)
        return self.function(*args)

def cleanPop(population):
    for p in population:
        if len(p.allels) == 0:
            p.allels = ["0"]
            print("Aqui no hay ningun problema")

def trydivide(a,b):
    if b!=0:
        return a/b
    else:
        return a/0.001
        #raise ZeroDivisionError


operatorTable = {'+' : Operator(2, lambda a,b: a+b),
                '-' : Operator(2, lambda a,b: a-b),
                '*': Operator(2, lambda a,b: a*b),
                '/': Operator(2, lambda a,b: trydivide(a,b))}

symbolTable = {
    "functions" : list(operatorTable.keys()),
    "terminals" : ['cte','x','y','z']
}

#Returns symbol info: arity or Operator object
##getArity('+') -> 2
##getArity('+', True) -> object(Operator)
def getArity(symbol):
    #Every function symbol has an operator object associated
    #print("type of symbol ", type(symbol))
    #print(symbolTable['terminals'])

    if symbol in operatorTable:
        return operatorTable[symbol].arity

    # Implies that if its not an operator, then is a VALID terminal
    else:
        return 0

def getFunction(symbol):
    return operatorTable[symbol]

def getSymbol(type):
    if type == 0:
        return random.choice(symbolTable["functions"])
    elif type == 1:
        return random.choice(symbolTable["terminals"])
    else:
        return random.choice(symbolTable["functions"]+symbolTable["terminals"])


#Returns max and mean fitness of a given population
def maxmeanFit(population):
    pop_len = len(population)
    fit_max = -99999999
    fit_acum = 0
    mean_len = 0
    best_individual = None

    for individual in population:
        fit_ind = individual.fitness
        #print(fit_ind)
        #print(type(fit_ind))
        fit_acum += fit_ind
        mean_len += len(individual.allels)

        if fit_ind > fit_max:
            fit_max = fit_ind
            best_individual = individual

    fit_acum /= pop_len
    mean_len /= pop_len

    print("Mejor individuo: ",fit_max," Puntuacion media ",fit_acum)
    print("Tamano medio del cromosoma: ", mean_len, " Tamano mejor individuo: ", len(best_individual.allels))

    return (fit_max, fit_acum, len(best_individual.allels), mean_len)

# Returns limit indexes of a given function
# Params:
##  c_allels: chromosome allels as list
##  i_head: leading index of the section
def getSection(c_allels, i_head):
    i_tail = i_head

    symbol = c_allels[i_head]

    #if symbol is terminal, then replace only a single element
    #else, replace the whole expression checking its arity
    if determineNode(symbol) is terminal_:
        return (i_head, i_tail)

    symbol_arity = getArity(symbol)

    remaining_symbols = symbol_arity

    #iterates through the expression to check its components
    while remaining_symbols > 0:
        i_tail += 1
        remaining_symbols -= 1

        additional_symbol = c_allels[i_tail]

        if additional_symbol not in symbolTable["terminals"]:

            additional_arity = getArity(additional_symbol)
            #extends remaining_symbols to include the implicit function
            remaining_symbols += additional_arity
    return (i_head, i_tail)

def determineNode(node):
    #Functions
    if node in symbolTable["functions"]:
        return 0
    #Terminals
    if node in symbolTable["terminals"]:
        #If 'cte', error
        if node is "cte":
            sys.exit("Error: 'cte' on a tree")
            return -1
        #Otherwise, terminal
        else:
            return 1
    #None of the above, guess it is a float
    return 1
