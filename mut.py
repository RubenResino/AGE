import random
import common
import init
from random import randint

def mutation (Chrom, treeDepth, maxNodes, notSimpleMutationRatio):

	#Parametros del problema:
    treeType = ['grow','full']
    #treeDepth = 0
    newOperatorArity = 0

    i = randint(0,len(Chrom)-1) #Se elige un alelo aleatorio del cromosoma.

    probToSimpleMutation = random.random()
    if probToSimpleMutation > notSimpleMutationRatio: #Un 60% de las veces se muta de forma simple, porcentaje arbitrario.
        if common.determineNode(Chrom[i]) is common.terminal_: #Si el alelo es un terminal... ## Posible correcion - se considera que un simbolo es terminal si no es una funcion
            Chrom[i] = (init.getRandomCte(random.choice(common.symbolTable['terminals']))) #Se sustituye por otro de la lista de terminales.
        else:
            #print(common.symbolTable['terminals'])
            while (common.getArity(Chrom[i]) != newOperatorArity): #Si es un operador, se sustituye por otro operadores de la MISMA aridad.
                newOperator = random.choice(common.symbolTable['functions'])
                newOperatorArity = common.getArity(newOperator)
            Chrom[i] = newOperator
    else:
        choosenTree = random.choice(treeType)
        #treeDepth = randint(2,9)
        newSubTree = init.initIndiv(choosenTree,treeDepth,maxNodes) #Llamada a la funcion que devuelve un nuevo subarbol
        if common.determineNode(Chrom[i]) is common.terminal_: #Si se inserta en un nodo hoja simplemente se sustituye por este.
            del Chrom[i]
            Chrom[i:i] = newSubTree
        else:
            index = common.getSection(Chrom,i) #Si no, se obtiene a traves de esta funcion la seccion del arbol que hay que reemplazar.
            del Chrom [index[0]:index[-1]+1] #Se borran esos indices del cromosoma.
            Chrom[i:i] = newSubTree #Se inserta el nuevo subarbol.
    #print(Chrom)
    return Chrom

"""TEST
test = [["+43"],["*x2"],["/zy"]]
result = mutation(test[0])
"""
