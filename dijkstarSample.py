from dijkstar import Graph, find_path
#creates a graph data structure which is basically a dictionary. undirected= True makes it an undirected graph
#which is the case for this assignment and network topologies in general.
graph=Graph(undirected=True)     

#add_edge makes an edge (or link in our case) between two nodes and their given cost.

graph.add_edge("A", "b", 1) 
graph.add_edge("A", "c", 1)
graph.add_edge("E", "d", 1)
graph.add_edge("E", "A", 1)

print(graph)

#find_path finds the path between two nodes given a graph. It returns a bunch of information which you can see printed below.
#Play around with the code below, try inputting a path that it can't find. 
#find_path returns an error if there is no path between the two specified nodes.
try: 
   path=find_path(graph,"b","d")
   print(path)
   print("PRINTING EVERYTHING INDIVIDUALLY")
   print("Nodes", path.nodes)
   print("Edges", path.edges)
   print("Costs", path.costs)
   print("Total cost", path.total_cost)
   print("Nodes", path.nodes[1])
   

except:
      print("path not found")

