from App.Code.Data_NodesAndEdgesFromDF.create_nodes_and_edges_from_df import SingleEdge

edge1 = SingleEdge('a', 'b')
edge2 = SingleEdge('a', 'b')
edge3 = SingleEdge('b', 'c')
print (edge1 == edge2)