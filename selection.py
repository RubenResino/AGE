import numpy as np

import random
import math

#population es un list con todas las instancias de Chromo que forman a una poblacion


#Metodo para elegir un individuo usando ruleta
def RouletteMethod(population, selective_pressure):
    popInicial=population      #Se guarda la poblacion recibida en popInicial
    numIndividuos = 0
    sumaMax = 0
    for individuo in popInicial:      #Se calcula el numero de individuos
       numIndividuos += 1
                                             
    individuoElegido = population[0]                                                #Se prepara indiviuoElegido, donde pondremos al que escogemos por medio de la ruleta (se inicializa por ahora con el primero de la poblacion)
    popOrdenada = sorted(popInicial, key=lambda x: x.fitness, reverse=True)         #Se ordena la poblacion por su fitness, de mayor a menor
    fitness_ruleta = []
   
    for i in range(numIndividuos):                                                  #Se calcula el fitness de ruleta proporcional a cada individuo según su ranking y se suma esa cantidad a la suma total de fitness
        fitness_ruleta.append (2 - selective_pressure + 2 * (selective_pressure - 1) * ((numIndividuos - i ) - 1 / numIndividuos - 1))
        sumaMax += (2 - selective_pressure + 2 * (selective_pressure - 1) * ((numIndividuos - i ) - 1 / numIndividuos - 1))
   
    numeroRandom = np.random.randint(sumaMax)                         #Se elige un numero alteatorio entre 0 y suma de fitness de ruleta
    
    
    individuoAntiguo = 0     #Se guardara en inviduoAntiguo la suma de fitness de los individuos comprobados por ahora en el loop
    individuoActual = 0
    #Se comprueba si el numero aleatorio pertenece al primer individuo (entre 0 y su valor de fitness), si no se comprueba si pertenece al segundo (entre el valor del primero y el valor conjunto del primero y el segundo),asi
    #hasta que se encuentre el individuo elegido en el que el numero aleatorio este en su intervalo (fitness hasta el individuo anterior, fitness con el indiviuo actual incluido), y se devuelve ese individuo
    for individuo in popOrdenada:
       if individuoAntiguo <= numeroRandom and (individuoAntiguo + fitness_ruleta[individuoActual]) > numeroRandom     :
          individuoElegido = individuo
          break
       else :
          individuoAntiguo += fitness_ruleta[individuoActual]
          individuoActual += 1

          
    #print ("Individuo escogido" , individuoElegido.fitness)     
    return individuoElegido.allels

#Metodo para eligir un individuo usando torneo
def tournament(population, t_size):


    pob_individuals = population                                                    #Se guarda la poblacion recibida en popIndividuals

    pob_fitsorted = sorted(population, key=lambda x: x.fitness, reverse=True)       #Se ordena la poblacion por su fitness



    best_fitness = -9999999999                                                      #En best_fitness se guardara el fitness del mejor individuo comprobado hasta ahora en el torneo

    individuoElegido = pob_individuals[0]                                           #Se prepara indiviuoElegido, donde pondremos al que escogemos por medio del torneo (se inicializa por ahora con el primero de la poblacion)
    #Por tantos individuos como tamano tenga el torneo, se elige un individuo de la poblacion aleatoriamente y si su fitness es mejor que la del mejor individuo, este se vuelve el mejor individuo y su fitness se vuelve la mejor fitness
    for i in range (t_size) :
       individuo_random = np.random.choice(pob_fitsorted, replace=False )
       if individuo_random.fitness > best_fitness:
          best_fitness = individuo_random.fitness
          individuoElegido = individuo_random
           

    #print ("Individuo escogido" , individuoElegido.fitness) 
    return individuoElegido.allels                       #Se devuelve el cromosoma del mejor individuo
      

"""
class Chromo:
    allels = []
    fitness = 0

    def __init__(self, allels = None):

        self.allels = []
        self.fitness = 0

        if allels is not None:
            self.allels = allels
"""
"""    
if __name__ == '__main__':
 
  population = []
  prueba1 = Chromo()
  prueba1.fitness = 50
  population.append (prueba1)
  prueba2 = Chromo()
  prueba2.fitness = 5000
  population.append (prueba2)
  prueba3 = Chromo()
  prueba3.fitness = 8
  population.append (prueba3)
  prueba4 = Chromo()
  prueba4.fitness = 100
  population.append (prueba4)
  prueba5 = Chromo()
  prueba5.fitness = -6
  population.append (prueba5)
  prueba6 = Chromo()
  prueba6.fitness = 0
  population.append (prueba6)
  prueba7 = Chromo()
  prueba7.fitness = 25
  population.append (prueba7)
  RouletteMethod (population, 1.5)
  tournament (population, 6)
"""