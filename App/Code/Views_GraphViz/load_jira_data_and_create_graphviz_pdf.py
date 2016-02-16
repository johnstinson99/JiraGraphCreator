from os.path import join

from App.Code.Data_NodesAndEdgesFromCSV.create_nodes_and_edges_from_csv import JiraReader
from App.Code.Views_GraphViz.jira_graphviz_drawer import GraphDrawer

my_dir = 'C:\\Users\\John\\Documents\\2016\\Python\\JiraStates'
f = join(my_dir, 'jira_states.csv')

my_jira_reader = JiraReader(f)
print(my_jira_reader)

my_graph_drawer = GraphDrawer(my_jira_reader)
my_graph_drawer.draw_chart()