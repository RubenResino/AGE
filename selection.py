import numpy as np
import requests
import random
import math

#population es un list con todas las instancias de Chromo que forman a una poblacion


#Metodo para elegir un individuo usando ruleta
def RouletteMethod(population):
    popInicial=population                                                           #Se guarda la poblacion recibida en popInicial
    sumaMax = 0
    for individuo in popInicial:                                                    #Se suma la fitness de todos los individuos
       sumaMax += individuo.fitness
    numeroRandom = np.random.randint(sumaMax)                                       #Se elije un valor aleatorio entre 0 y la suma de los fitness
    individuoElegido = population[0]                                                #Se prepara indiviuoElegido, donde pondremos al que escogemos por medio de la ruleta (se inicializa por ahora con el primero de la poblacion)
    popOrdenada = sorted(popInicial, key=lambda x: x.fitness, reverse=True)         #Se ordena la poblacion por su fitness, de mayor a menor
    individuoAntiguo = 0                                                            #Se guardara en inviduoAntiguo la suma de fitness de los individuos comprobados por ahora en el loop
    #Se comprueba si el numero aleatorio pertenece al primer individuo (entre 0 y su valor de fitness), si no se comprueba si pertenece al segundo (entre el valor del primero y el valor conjunto del primero y el segundo),asi
    #hasta que se encuentre el individuo elegido en el que el numero aleatorio este en su intervalo (fitness hasta el individuo anterior, fitness con el indiviuo actual incluido), y se devuelve ese individuo
    for individuo in popOrdenada:
       if individuoAntiguo <= numeroRandom and (individuoAntiguo + individuo.fitness) > numeroRandom	   :
          individuoElegido = individuo
          break
       else :
          individuoAntiguo += individuo.fitness

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



    return individuoElegido.allels                       #Se devuelve el cromosoma del mejor individuo
