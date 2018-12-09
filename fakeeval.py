import random, requests

def evaluate(chromo):
  #chromo.fitness = random.uniform(0, 1) * random.randint(0, 100)
  n_requests = 10
  evaluation = 0

  # Each evaluation consists of n_requests requests to the server
  for i in range(n_requests):
      days = 0
      seats = 0
      demand = 0
      price = 0

      # Generates dummy values for evaluation
      days = random.randint(1, 365)
      seats = random.randint(1, 500)
      demand = random.randint(0, 100)
      price = random.randint(1, 2000)

      # Server response is fitness
      url = "http://memento.evannai.inf.uc3m.es/age/eci1?days={}&seats={}&demand={}&price={}".format(days, seats, demand, price)
      #print(requests.get(url).text)
      evaluation += float(requests.get(url).text)
      #print(evaluation, days, seats, demand, price)


  evaluation /= n_requests

  return evaluation
