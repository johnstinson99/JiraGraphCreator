from os.path import join
from App.Code.JiraToGraph.jira_graph_creator import JiraReader, GraphDrawer

my_dir = 'C:\\Users\\John\\Documents\\2016\\Python\\JiraStates'
f = join(my_dir, 'jira_states.csv')

my_jira_reader = JiraReader(f)
print(my_jira_reader)

my_graph_drawer = GraphDrawer(my_jira_reader)
my_graph_drawer.draw_chart()