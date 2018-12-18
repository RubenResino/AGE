import numpy as np
import requests
import random
import math
import common
import concurrent.futures

np.set_printoptions(threshold=np.nan)

#Carga de los ejemplos de entrenamiento
inputs=np.genfromtxt('def_evaluation.csv', delimiter=',').astype(int)

#Funcion de parseo
def prefixParse(code,a,b,c):
    #Obtenemos el primer elemento
    token=code[0]

    #Si el token es una operacion
    if token in common.symbolTable["functions"]:

        arity = common.getArity(token)
        operator = common.getFunction(token)

        #Si la operacion es de aridad 2 (tipo a+b)
        if arity == 2:
            #Calculas el valor de las dos ramas que opera
            arg1, chomp1 = prefixParse(code[1:],a,b,c)
            arg2, chomp2 = prefixParse(code[chomp1 + 1:],a,b,c)
            #Devuelves el resultado y el tamano de esta rama
            try:
                return operator(arg1, arg2), chomp1 + chomp2 + 1
            except ZeroDivisionError:
                raise ZeroDivisionError
        #Si la operacion es de aridad 1 (tipo -a)
        elif operator.arity == 1:
            #Calculas el valor de la rama que opera
            arg, chomp = prefixParse(code[1:],a,b,c)
            #Devuelves el resultado y el tamano de esta rama
            try:
                return operator(arg), chomp + 1
            except ZeroDivisionError:
                raise ZeroDivisionError
        #Si la operacion es de aridad 0 (constantes)
        elif operator.arity == 0:
            #Devuelve el valor de la constante y el tamano de la rama (1)
            return operator(), 1
    #Si no es una operación (se comporta igual que aridad 0)
    else:                   #elif token in common.symbolTable["terminals"]:
        #Si es una incognita devuelve el valor de la incognita
        if token=='x':
            return a, 1
        elif token=='y':
            return b, 1
        elif token=='z':
            return c, 1
        #Si no, es numero y devuelve su valor (y si no, alguien la ha cagado)
        else:
            return float(token), 1

#Llamada al servidor
def load_url(url, timeout):
    ans = requests.get(url, timeout=timeout)
    return float(ans.text)


def evaluate(chromosome):
    out = []
    CONNECTIONS = 12   # Number of threads to use
    TIMEOUT = 10
    urls = []
    '''
    fitness=0
    for inp in inputs:
        try:
            price=int(prefixParse(chromosome.allels, inp[0], inp[1], inp[2])[0])
        except ZeroDivisionError:
            return -1000000
        if price<0:
            return -100000

        fitness+=float(requests.get("http://memento.evannai.inf.uc3m.es/age/eci1?days={}&seats={}&demand={}&price={}".format(inp[0],inp[1],inp[2],price)).text)
    return fitness/100
    '''
    #Calculo del precio para todos los ejemplos de entrenamiento
    for i, inp in enumerate(inputs):
        try:
            price=int(prefixParse(chromosome.allels, inp[0], inp[1], inp[2])[0])
            if price<0:
                price=0
                #return -100000
            urls.append("http://memento.evannai.inf.uc3m.es/age/eci1?days={}&seats={}&demand={}&price={}".format(inp[0],inp[1],inp[2],price))
        except ZeroDivisionError:
            return -1000000

    #LLamadas al servidor en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers = CONNECTIONS) as executor:
        #future_to_url = (executor.submit(load_url, url) for url in urls)

        m=list(executor.map(load_url,urls,np.repeat(TIMEOUT,len(inputs))))
        media = np.mean(m)
        return media
        #executor.wait(future_to_url, timeout=TIMEOUT, return_when=ALL_COMPLETED)

        #mean = np.mean(future_to_url.result())


        '''
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                # out response
                out.append(data)

                #print(str(len(out)),end="\r")
        '''


'''
data=np.empty([10000,4])
i=0
random.seed(42)
while i<10000:



    d1=random.randint(1,365)
    d2=random.randint(1,500)
    d3=random.randint(0,100)
    d4=random.randint(1,1000)
    r=requests.get("http://memento.evannai.inf.uc3m.es/age/eci1?days={}&seats={}&demand={}&price={}".format(d1,d2,d3,d4))
    r_float=float(r.text)

    #print(aux_arr)

    if r_float not in data[:,3]:
        print(i)
        data[i]=np.array([d1,d2,d3,r_float])
        i+=1

print(data)
np.savetxt("def_evaluation_2.csv", data, delimiter=",")
'''

#prueba = ['+', '7', '+', '/', '+', 'y', '*', 'y', 'z', '-', '/', 'x', 'y', 'z', '+', '+', '-', 'y', 'z', 'x', '3.615', '-', '5.632', '-', '-', '-', '+', 'z', 'y', 'x', '5.855', '/', 'z', 'z', 'x']

#prefixParse(prueba,1,2,3)
#c=common.Chromo()
#c.allels="/y+xz"
#print(c.allels)
#print(evaluate(c))
