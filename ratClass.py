class Rat:
  def __init__(self, sex, weight, litters=0):
    self.sex = sex
    self.weight = weight
    self.litters = litters
  def __str__(self):
    return f"({self.sex}) - {self.weight}g"
  def __repr__(self):
    return f"({self.sex}, {self.weight})"
  def getWeight(self):
    return self.weight
  def getSex(self):
    return self.sex
  def canBreed(self, LITTER_SIZE):
    return self.litters < LITTER_SIZE * 5
  def __lt__(self, x):
    return self.weight < x
  def __gt__(self, x):
    return self.weight > x
  def __le__(self, x):
    return self.weight <= x 
  def __ge__(self, x):
    return self.weight >= x
  def __eq__(self, x):
    return self.weight == x
