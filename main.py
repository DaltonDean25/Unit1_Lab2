import matplotlib.pyplot as plt

def readFile(fileName):
  f = open(fileName, 'r')
  data = f.read()
  f.close()

  data = orgFileData(data)

  return data

def orgFileData(data):
  data = data.split(', ')
  numData = []
  for num in data:
    numData.append(int(num))
  return numData

def createGraph(dataSet):
  plt.plot(dataSet)

  plt.title('Rat Growth')
  plt.xlabel('Generation')
  plt.ylabel('Rat Weight (grams)')
  plt.legend(["Average Mean", "Largest Rat", "Smallest Rat"])

  plt.show()
  plt.savefig('sample.png')

def main():
  files = ["AvgRatMeans.txt", "LargestRats.txt", "SmallestRats.txt"]

  allMeans = readFile(files[0])
  allLargest = readFile(files[1])
  allSmallest = readFile(files[2])

  for dataSet in [allMeans, allLargest, allSmallest]:
    createGraph(dataSet)

if __name__ == "__main__":
  main()