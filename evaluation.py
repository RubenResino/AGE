import numpy as np
import requests
import random
import math
import common
import concurrent.futures

np.set_printoptions(threshold=np.nan)
inputs=np.genfromtxt('def_evaluation.csv', delimiter=',').astype(int)


def prefixParse(code,a,b,c):
    token=code[0]

    if token in common.symbolTable["functions"]:

        arity = common.getArity(token)
        operator = common.getFunction(token)

        if arity == 2:
            arg1, chomp1 = prefixParse(code[1:],a,b,c)
            arg2, chomp2 = prefixParse(code[chomp1 + 1:],a,b,c)
            try:
                return operator(arg1, arg2), chomp1 + chomp2 + 1
            except ZeroDivisionError:
                raise ZeroDivisionError

        elif operator.arity == 1:
            arg, chomp = prefixParse(code[1:],a,b,c)
            try:
                return operator(arg), chomp + 1
            except ZeroDivisionError:
                raise ZeroDivisionError

        elif operator.arity == 0:
            return operator(), 1

    elif token in common.symbolTable["terminals"]:
        if token=='x':
            return a, 1
        elif token=='y':
            return b, 1
        elif token=='z':
            return c, 1
        else:
            return int(token), 1

def load_url(url, timeout):
    ans = requests.get(url, timeout=timeout)
    return float(ans.text)


def evaluate(chromosome):
    out = []
    CONNECTIONS = 100   # Number of threads to use
    TIMEOUT = 5
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
    for i, inp in enumerate(inputs):
        try:
            price=int(prefixParse(chromosome.allels, inp[0], inp[1], inp[2])[0])
            if price<0:
                return -100000
            urls.append("http://memento.evannai.inf.uc3m.es/age/eci1?days={}&seats={}&demand={}&price={}".format(inp[0],inp[1],inp[2],price))
        except ZeroDivisionError:
            return -1000000

    with concurrent.futures.ThreadPoolExecutor(max_workers = CONNECTIONS) as executor:
        #future_to_url = (executor.submit(load_url, url) for url in urls)

        m=list(executor.map(load_url,urls,np.ones(100)))
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
data=np.empty([100,4])
i=0
random.seed(42)
while i<100:



    d1=random.randint(1,365)
    d2=random.randint(1,500)
    d3=random.randint(0,100)
    d4=random.randint(5,100)
    r=requests.get("http://memento.evannai.inf.uc3m.es/age/eci1?days={}&seats={}&demand={}&price={}".format(d1,d2,d3,d4))
    r_float=float(r.text)

    #print(aux_arr)

    if r_float not in data[:,3]:
        data[i]=np.array([d1,d2,d3,r_float])
        i+=1

print(data)
np.savetxt("def_evaluation.csv", data, delimiter=",")

'''

c=common.Chromo()
c.allels="/y+xz"
print(c.allels)
print(evaluate(c))
