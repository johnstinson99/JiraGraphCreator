from App.Code.Data_NodesAndEdgesFromCSV.create_nodes_and_edges_from_csv import SingleEdge

edge1 = SingleEdge('a', 'b')
edge2 = SingleEdge('a', 'b')
edge3 = SingleEdge('b', 'c')
print (edge1 == edge2)