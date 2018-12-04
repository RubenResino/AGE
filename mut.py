import random
import common
import init
from random import randint
  			
def mutation (unmut_chrom):

    treeType = ['grow','full']
    treeDepth = 0
    notSimpleMutationRatio = 0.4
    newOperatorArity = 0
    """
    strChrom = ''.join(unmut_chrom)
    Chrom = list(strChrom)
    """
    i = randint(0,len(Chrom)-1)

    probToSimpleMutation = random.random()
    if probToSimpleMutation > notSimpleMutationRatio:
        if Chrom[i] in common.symbolTable['terminals']:
            Chrom[i] = (init.getRandomCte(random.choice(common.symbolTable['terminals'])))
        else:
            while (common.getArity(Chrom[i]) != newOperatorArity):
                newOperator = random.choice(common.symbolTable['functions'])
                newOperatorArity = common.getArity(newOperator)
            Chrom[i] = newOperator
    else:
        choosenTree = random.choice(treeType)
        treeDepth = randint(9,9)
        newSubTree = init.initIndiv(treeDepth,choosenTree) #Llamada a la funcion que devuelve in individuo
        strNewSubTree = ''.join(newSubTree)
        if Chrom[i] in common.symbolTable['terminals']:
            Chrom[i] = strNewSubTree
        else:
            index = common.getSection(Chrom,i)
            del Chrom [index[0]+1:index[-1]+1]
            Chrom[i] = strNewSubTree

    strChrom =''.join(Chrom)
    Chrom = list(strChrom)
    print(Chrom)
    return Chrom


test = [["+43"],["*x2"],["/zy"]]
result = mutation(test[0])




        

