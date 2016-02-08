from App.Code.JiraToGraph.jira_graph_creator import SingleEdge

edge1 = SingleEdge('a', 'b')
edge2 = SingleEdge('a', 'b')
edge3 = SingleEdge('b', 'c')
print (edge1 == edge2)