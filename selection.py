import numpy as np
import requests
import random
import math

#population es un list con todas las instancias de Chromo que forman a una poblacion

def RouletteMethod(population):
    popInicial=population
    sumaMax = 0
    for individuo in popInicial:
       sumaMax += individuo.fitness
    numeroRandom = np.random.randint(sumaMax)
    individuoElegido = population[0]
    popOrdenada = sorted(popInicial, key=lambda x: x.fitness, reverse=True)
    individuoAntiguo = 0
    for individuo in popOrdenada:
       if individuoAntiguo <= numeroRandom and (individuoAntiguo + individuo.fitness) > numeroRandom	   :
          individuoElegido = individuo
          break
       else :
          individuoAntiguo += individuo.fitness

    return individuoElegido

def tournament(population, t_size):
    n_rounds = 1

    pob_individuals = population
    S_POBLATION = len(population)
    pob_fitsorted = sorted(population, key=lambda x: x.fitness, reverse=True)
    individuoElegido = population[0]


    best_fitness = -9999999999

    individuoElegido = pob_individuals[0]
    for i in range (t_size) :
       individuo_random = np.random.choice(pob_fitsorted, replace=False )
       if individuo_random.fitness > best_fitness:
          best_fitness = individuo_random.fitness
          individuoElegido = individuo_random

    return individuoElegido.allels
