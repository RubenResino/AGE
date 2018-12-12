import common
import random
#~~~Crossing codification~~~
"""
-Select some specific nodes (random indices) (in pairs; can be swapped in different regions of each Chromo)
-check the length of the referenced subtrees (n of allels to move)
-keep subtrees to swap and indices
-remove subtrees from original Chromos
-push subtrees into crossed
"""

#gets the corresponding bounds inside a function given:
##chromo (function ~ individual)
##i_head index of the symbol inside the function

#Given a chromosome and a tuple representing the indices of the section to get, returns the allels inside the section
def getBlocks(chromo, i_section):
    return chromo[i_section[0] : i_section[1] + 1]


#this should take a tuple of individuals
#no return needed. Operates over references
def love(parents, n_swaps = 1):
    # Method will operate over the original data

    #As many crossings as specify in n_swaps
    #Swaping must be done individually, since every time a swap occurs between chromosomes, its size changes
    for swap in range(n_swaps):

        #gets random indices (valid across both individuals)
        crosspoints = (random.randint(0, len(parents[0]) - 1), random.randint(0, len(parents[1]) - 1))

        #nested tuples
        #the outter tuple represents each of the parents crossing sections
        #inner tuple (getSection return) represents the begining and ending of the section
        bounds = (common.getSection(parents[0], crosspoints[0]), common.getSection(parents[1], crosspoints[1]))

        #actual blocks of symbols to swap between parents
        blocks = (getBlocks(parents[0], bounds[0]), getBlocks(parents[1], bounds[1]))

        #print("First parent block:\n", blocks[0], "\n-bounds: ", bounds[0])
        #print("Second parent block:\n", blocks[1], "\n-bounds: ", bounds[1])

        # love begins here
        # using python comprehension:
        ## list = [r, a, w, r, t, a, s, t, i, c]
        ## list[2 : 7] = 42
        ## list -> [r, a, 42, t, i, c]
        parents[0][bounds[0][0] : bounds[0][1] + 1] = blocks[1]
        parents[1][bounds[1][0] : bounds[1][1] + 1] = blocks[0]

    return parents

"""
#fart
dummy = "+-5+42+37" # (5 - (4 + 2)) + (3 + 7)
dummy2 = "-+/35*42/52"                    # ((3 / 5) + (4 * 2)) - (5 / 2)

d_individual = common.Chromo(dummy)
d_individual2 = common.Chromo(dummy2)

myindividuals = [d_individual, d_individual2]
print("Pre crossing:\n", d_individual.allels, "\n", d_individual2.allels, "\n\n")

love(myindividuals)
print("Post crossing:\n", d_individual.allels, "\n", d_individual2.allels, "\n")
"""
