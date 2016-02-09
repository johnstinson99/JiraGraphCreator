import networkx as nx
import matplotlib.pyplot

G = nx.DiGraph()

G.add_node(1, time = '5pm')
G.add_nodes_from([2,3])
G.add_node('spam')

G.add_edge(1,2, weight = 4.3, color = 'red')
G.add_edge(1,3)
print('No of nodes = ' + str(G.number_of_nodes()))
print('Nodes:')
print(G.nodes())
print('Edges:')
print(G.edges())
print('Neighbours of 1:')
print(G.neighbors(1))

# nx.draw(G)
d = nx.to_pydot(G)
# nx.write_dot(G, 'C:\\Users\\John\\Documents\\2016\\Python\\GraphViz\myfile.dot')  # need to convert pydot from Python2 to 3