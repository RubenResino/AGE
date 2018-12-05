import random
import common
import init
from random import randint

def mutation (Chrom):

	#Parámetros del problema:
    treeType = ['grow','full']
    treeDepth = 0
    notSimpleMutationRatio = 0.4
    newOperatorArity = 0

    i = randint(0,len(Chrom)-1) #Se elige un alelo aleatorio del cromosoma.

    probToSimpleMutation = random.random()
    if probToSimpleMutation > notSimpleMutationRatio: #Un 60% de las veces se muta de forma simple, porcentaje arbitrario.
        if Chrom[i] in common.symbolTable['terminals']: #Si el alelo es un terminal...
            Chrom[i] = (init.getRandomCte(random.choice(common.symbolTable['terminals']))) #Se sustituye por otro de la lista de terminales.
        else:
            print(common.symbolTable['terminals'])
            while (common.getArity(Chrom[i]) != newOperatorArity): #Si es un operador, se sustituye por otro operadores de la MISMA aridad.
                newOperator = random.choice(common.symbolTable['functions'])
                newOperatorArity = common.getArity(newOperator)
            Chrom[i] = newOperator
    else:
        choosenTree = random.choice(treeType)
        treeDepth = randint(2,9)
        newSubTree = init.initIndiv(treeDepth,choosenTree) #Llamada a la funcion que devuelve un nuevo subárbol
        strNewSubTree = ''.join(newSubTree)
        if Chrom[i] in common.symbolTable['terminals']: #Si se inserta en un nodo hoja simplemente se sustituye por este.
            Chrom[i] = strNewSubTree
        else:
            index = common.getSection(Chrom,i) #Si no, se obtiene a través de esta función la sección del árbol que hay que reemplazar.
            del Chrom [index[0]+1:index[-1]+1] #Se borran esos índices del cromosoma.
            Chrom[i] = strNewSubTree #Se inserta el nuevo subárbol.

    strChrom =''.join(Chrom)
    Chrom = list(strChrom) #Se transforma el individuo al formato que tiene Chrom.allels.
    print(Chrom)
    return Chrom

""" TEST
test = [["+43"],["*x2"],["/zy"]]
result = mutation(test[0])
"""
