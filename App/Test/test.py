from graphviz import Graph
import pandas as pd
from os.path import join


my_dir = 'C:\\Users\\John\\Documents\\2016\\Python\\JiraStates'
full_jira_df = pd.read_csv(join(my_dir, 'jira_states.csv'))
# print(df)

issue_list = pd.Series.unique(full_jira_df["IssueNo"])
print(issue_list)



mygraph = Graph('ER', filename='test.gv', engine='circo')

# FIRST SET UP THE NODES
mygraph.attr('node', shape='ellipse', width='10')
mygraph.node('name0', label='name', color='red', width='10')
mygraph.node('name1', label='name')


#NOW JOIN THE NODES WITH EDGES
mygraph.edge('name0', 'name1', color='blue', dir='forward', edgetooltip='a tool tip')



#FINALLY DISPLAY THE GRAPH
mygraph.view()