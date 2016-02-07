import pandas as pd
from os.path import join
from graphviz import *

class edge:

    count = 0

    def __init__(self, my_from_string, my_to_string):
        self.from_string = my_from_string
        self.to_string = my_to_string

    def __str__(self):
        return ("edge: " + self.from_string + " -> " + self.to_string)

    # def __eq__(self, other):
    #     return(self.to_string == other.to_string & self.from_string == other.from_string)

class jira_reader:
    def __init__(self, my_file_and_path_string):
        self.file_and_path_string = my_file_and_path_string
        self.jira_df = pd.read_csv(my_file_and_path_string)
        self.issue_list = pd.Series.unique(self.jira_df['IssueNo'])
        self.state_list = pd.Series.unique(self.jira_df['To'])
        edge_df = self.jira_df[['From', 'To']]
        self.edge_object_list = set([edge(row[0], row[1]) for row in edge_df.values if row[0] != 'Undefined'])

    def __str__(self):
        str1 = 'df = \n' + str(self.jira_df) + '\n'
        str2 = 'issue_list = ' + str(self.issue_list) + '\n'
        str3 = 'state_list = ' + str(self.state_list) + '\n'
        # str4 = 'edge_tuple_set = ' + str(self.edge_tuple_set) + '\n'
        str4 = 'edge_object_list = \n'
        for my_edge in self.edge_object_list:
            print(my_edge)
        return(str1 + str2 + str3 + str4)

    def create_chart(self):
        # SET UP THE GRAPH
        self.graph = Graph('Jira Chart', filename='jira_chart.gv', engine='circo')
        self.graph.attr('node', shape = 'ellipse')  # width = '10',  color = 'red'

        # SET UP THE NODES
        for my_node in self.state_list:
            self.graph.node(my_node)
            # mygraph.node('name0', label='name', color='red', width='10')

        #NOW JOIN THE NODES WITH EDGES
        # mygraph.edge('name0', 'name1', color='blue', dir='forward', edgetooltip='a tool tip')
        for my_edge in self.edge_object_list:
            self.graph.edge(my_edge.from_string, my_edge.to_string, dir = 'forward')

        #FINALLY DISPLAY THE GRAPH
        self.graph.view()



my_dir = 'C:\\Users\\John\\Documents\\2016\\Python\\JiraStates'
f = join(my_dir, 'jira_states.csv')
my_jira_reader = jira_reader(f)
print(my_jira_reader)
my_jira_reader.create_chart()