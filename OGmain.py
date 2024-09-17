#Dalton Dean
#Unit 1 lab 1
#Simulation that breeds rats until the rat population reaches a mean of 50,000 grams
from ratClass import Rat
from random import triangular, randint, choice
from time import time

GOAL = 50000                # Target average weight (grams)
NUM_RATS = 20               # Max adult rats in the lab
INITIAL_MIN_WT = 200        # The smallest rat (grams)
INITIAL_MAX_WT = 600        # The chonkiest rat (grams)
INITIAL_MODE_WT = 300       # The most common weight (grams)
MUTATE_ODDS = 0.01          # Liklihood of a mutation
MUTATE_MIN = 0.5            # Scalar mutation - least beneficial
MUTATE_MAX = 1.2            # Scalar mutation - most beneficial
LITTER_SIZE = 8             # Pups per litter (1 mating pair)
GENERATIONS_PER_YEAR = 10   # How many generations are created each year
GENERATION_LIMIT = 500      # Generational cutoff - stop breeded no matter what

def writeFile(fileName, data):
  f = open(fileName, 'w')
  f.write(", ".join(data))
  f.close()


def initial_population():
  '''Create the initial set of rats based on constants'''
  rats = [[],[]]
  mother = Rat("F", INITIAL_MIN_WT)
  father = Rat("M", INITIAL_MAX_WT)
  
  for r in range(NUM_RATS):
    if r < 10:
      sex = "M"
      ind = 0
    else:
      sex = "F"
      ind = 1

    wt = calculate_weight(sex, mother, father)
    R = Rat(sex, wt)
    rats[ind].append(R)
  
  return rats

def calculate_weight(sex, mother, father):
  '''Generate the weight of a single rat'''
  if father > mother:
    max = father.getWeight()
    min = mother.getWeight()
  else:
    max = mother.getWeight()
    min = father.getWeight()
  
  if sex == "M":
    wt = int(triangular(min, max, max))
  else:
    wt = int(triangular(min, max, min))

  return wt

def mutate(pups):
  """Check for mutability, modify weight of affected pups"""
  for pup in (pups[0] + pups[1]):
    if randint(1, 100) == MUTATE_ODDS * 100:
      factor = randint(MUTATE_MIN * 100, MUTATE_MAX * 100) / 100
      pup.weight = int(pup.getWeight() * factor)

  return pups  

def breed(rats):
  """Create mating pairs, create LITTER_SIZE children per pair"""
  children = [[], []]

  for pairing in range(0, int(NUM_RATS/2)):
    father = rats[0][pairing]
    mother = rats[1][pairing]

    for r in range(0, LITTER_SIZE):
      sex = choice(['M', 'F'])
      if sex == 'M':
        ind = 0
      else:
        ind = 1

      father.litters += LITTER_SIZE
      mother.litters += LITTER_SIZE
      wt = calculate_weight(sex, mother, father)
      R = Rat(sex, wt)
      children[ind].append(R)

  return children  

def select(rats, pups):
  '''Choose the largest viable rats for the next round of breeding'''
  maleRats = rats[0] + pups[0]
  femaleRats = rats[1] + pups[1]

  rats = [[], []]

  while len(rats[0]) != NUM_RATS / 2:
    largest = max(maleRats)
    if largest.canBreed(LITTER_SIZE):
      rats[0].append(largest)
    maleRats.remove(largest)
  while len(rats[1]) != NUM_RATS / 2:
    largest = max(femaleRats)
    if largest.canBreed(LITTER_SIZE):
      rats[1].append(largest)
    femaleRats.remove(largest)
  
  if rats[0][0] > rats[1][0]:
    largest = rats[0][0]
  else:
    largest = rats[1][0]
  if min(maleRats) < min(femaleRats):
    smallest = min(maleRats)
  else:
    smallest = min(femaleRats)
  

  return rats, largest, smallest

def calculate_mean(rats):
  '''Calculate the mean weight of a population'''
  sumWt = 0

  for rat in (rats[0] + rats[1]):
    sumWt += rat.getWeight()

  return sumWt // NUM_RATS

def fitness(rats):
  """Determine if the target average matches the current population's average"""
  mean = calculate_mean(rats)

  return mean >= GOAL, mean

def main():
  start = time()
  rats = initial_population()
  GENERATION = 0
  years = 0
  goalReached = False
  allMeans = []
  allLargest = []
  allSmallest = []

  while not goalReached:
    pups = breed(rats)
    pups = mutate(pups)
    rats, largest, smallest = select(rats, pups)
    goalReached, mean = fitness(rats)
      
    allMeans.append(str(mean))
    allLargest.append(str(largest.getWeight()))
    allSmallest.append(str(smallest.getWeight()))
    GENERATION += 1
  end = time()
  print("~~~~~~~~~ Results ~~~~~~~~~\n")
  
  print(f"Final Population Mean: {allMeans[-1]}\n")
  print(f"Generations: {GENERATION}")
  print(f"Experiment Duration: ~{int(GENERATION/GENERATIONS_PER_YEAR)} years")
  print(f"Simulation Duration: {round(end - start, 4)} seconds\n")

  print(f"✨  The Largest Rat ✨\n🐀  {largest}\n\n")
  print("Generation Weight Averages (grams)\n")

  for m in allMeans:
    m = str(m)
    if len(m) == 3:
      print(m, end="   ")
    elif len(m) == 4:
      print(m, end="  ")
    else:
      print(m, end=" ")

  print()

  #File Writing
  writeFile("AvgRatMeans.txt", allMeans)
  writeFile("LargestRats.txt", allLargest)
  writeFile("SmallestRats.txt", allSmallest)

if __name__ == "__main__":
  main()