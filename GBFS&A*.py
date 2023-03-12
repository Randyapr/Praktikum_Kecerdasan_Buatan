import queue
import matplotlib.pyplot as plt

# ngambil heuristik di file
def getHeuristics():
  heuristics = {}
  f = open("Romanian Problem/heuristics.txt")
  for i in f.readlines():
    node_heuristic_val = i.split()
    heuristics[node_heuristic_val[0]] = int(node_heuristic_val[1])
  
  return heuristics

# lokasi cities dari file
def getCity():
  city = {}
  citiesCode = {}
  f = open("Romanian Problem/cities.txt")
  j = 1
  for i in f.readlines():
    node_city_val = i.split()
    city[node_city_val[0]] = [int(node_city_val[1]), int(node_city_val[2])]

    citiesCode[j] = node_city_val[0]
    j += 1
  return city, citiesCode

#graph di file
def createGraph():
  graph = {}
  file = open("Romanian Problem/citiesGraph.txt")
  for i in file.readlines():
    node_val = i.split()

    if node_val[0] in graph and node_val[1] in graph:
      c = graph.get(node_val[0])
      c.append([node_val[1], node_val[2]])
      graph.update({node_val[0]: c})
    
    elif node_val[0] in graph:
      c = graph.get(node_val[0])
      c.append([node_val[1], node_val[2]])
      graph.update({node_val[0]: c})

      graph[node_val[1]] = [[node_val[0], node_val[2]]]
    
    elif node_val[1] in graph:
      c = graph.get(node_val[1])
      c.append([node_val[0], node_val[2]])
      graph.update({node_val[1]: c})

      graph[node_val[0]] = [[node_val[1], node_val[2]]]
    
    else:
      graph[node_val[0]] = [[node_val[1], node_val[2]]]
      graph[node_val[1]] = [[node_val[0], node_val[2]]]
  
  return graph

#Algoritma GBFS
def GBFS(startNode, heuristics, graph, goalNode="Bucharest"):
  priorityQueue = queue.PriorityQueue()
  priorityQueue.put((heuristics[startNode], startNode))
  path = []

  while priorityQueue.empty() == False:
    current = priorityQueue.get()[1]
    path.append(current)
    
    if current == goalNode:
      break
    
    priorityQueue = queue.PriorityQueue()

    for i in graph[current]:
      if i[0] not in path:
        priorityQueue.put((heuristics[i[0]], i[0]))

  return path

# gambar map 
def drawMap(city, gbfs, graph):
  for i, j in city.items():
    plt.plot(j[0], j[1], "ro")
    plt.annotate(i, (j[0] +5, j[1]))

    for k in graph[i]:
      n = city[k[0]]
      plt.plot([j[0], n[0]], [j[1], n[1]], "gray")
  
  for i in range(len(gbfs)):
    try:
      first = city[gbfs[i]]
      secend = city[gbfs[i + 1]]

      plt.plot([first[0], secend[0]], [first[1], secend[1]], "green")
    except:
      continue
  
  plt.errorbar(1,1, label="GBFS", color="green")
  plt.legend(loc="lower left")

  plt.show()

#run program
def main():
  heuristic = getHeuristics()
  graph = createGraph()
  city, citiesCode = getCity()

  for i, j in citiesCode.items():
    print(i, j)

  while True:
    inputCode = int(input("Masukkan Nomor Kota Asal (0 untuk keluar) : "))

    if inputCode == 0:
      break
    
    cityName = citiesCode[inputCode]

    gbfs = GBFS(cityName, heuristic, graph, goalNode="Bucharest")
    print("GBFS => ", gbfs)

    drawMap(city, gbfs, graph)
main()
# Algoritma A*
def Astar(startNode, heuristics, graph, goalNode="Bucharest"):
  priorityQueue = queue.PriorityQueue()
  distance = 0
  path = []

  priorityQueue.put((heuristics[startNode] + distance, [startNode, 0]))
  while priorityQueue.empty() == False:
    current = priorityQueue.get()[1]
    path.append(current[0])
    distance += int(current[1])

    if current[0] == goalNode:
      break

    for i in graph[current[0]]:
      if i[0] not in path:
        priorityQueue.put((heuristics[i[0]] + int (i[1]) + distance, i))
  return path
def drawMap(city, gbfs, astar, graph):
  for i, j in city.items():
    plt.plot(j[0], j[1], "ro")
    plt.annotate(i, (j[0] + 5, j[1]))

    for k in graph[i]:
      n = city[k[0]]
      plt.plot([j[0], n[0]], [j[1], n[1]], "gray")

  for i in range(len(gbfs)):
    try:
      first = city[gbfs[i]]
      secend = city[gbfs[i + 1]]

      plt.plot([first[0], secend[0]], [first[1], secend[1]], "green")
    except:
        continue
  for i in range(len(astar)):
    try:
      first = city[astar[i]]
      secend = city[astar[i +1]]

      plt.plot([first[0], secend[0]], [first[1], secend[1]], "blue")
    except:
      continue
  plt.errorbar(1, 1, label="GBFS", color="green")
  plt.errorbar(1, 1, label="ASTAR", color="blue")

  plt.show()
def main():
  heuristic = getHeuristics()
  graph = createGraph()
  city, citiesCode = getCity()

  for i, j in citiesCode.items():
    print(i, j)

  while True:
    inputCode = int(input("Masukkan nomor KOTA ASAL (0 untuk keluar):"))

    if inputCode == 0:
      break
    cityName = citiesCode[inputCode]

    gbfs = GBFS(cityName, heuristic, graph)
    astar = Astar(cityName, heuristic, graph)
    print("GBFS => ", gbfs)
    print("ASTAR =>", astar)

    drawMap(city, gbfs, astar, graph)

main()
