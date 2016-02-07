from App.Code.JiraToGraph.jira_graph_creator import edge

edge1 = edge('a', 'b')
edge2 = edge('a', 'b')
edge3 = edge('b', 'c')
print (edge1 == edge2)