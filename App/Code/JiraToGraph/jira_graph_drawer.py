from graphviz import *

class GraphDrawer:

    def __init__(self, jira_reader):
        self.graph = Graph('Jira Graph', filename='jira_graph.gv', engine='fdp')   #circo fdp neato
        self.graph.attr('node', shape = 'ellipse')  # width = '10',  color = 'red'

        # SET UP THE NODES
        for my_node in jira_reader.unique_node_list:
            self.graph.node(my_node)
            # mygraph.node('name0', label='name', color='red', width='10')

        #NOW JOIN THE NODES WITH EDGES
        # mygraph.edge('name0', 'name1', color='blue', dir='forward', edgetooltip='a tool tip')
        for my_combined_edge in jira_reader.unique_combined_edge_list:
            self.graph.edge(my_combined_edge.from_string,
                            my_combined_edge.to_string,
                            dir = 'forward',
                            # label = str(my_combined_edge.count) + ", " + str(int(my_combined_edge.day_diff_50_percentile)),
                            label = str(int(my_combined_edge.day_diff_50_percentile)) + "d Median",
                            penwidth = str(my_combined_edge.width_0_to_1 * 5),
                            len = str(my_combined_edge.day_diff_50_percentile_0_to_1 * 5))

    def draw_chart(self):
        #FINALLY DISPLAY THE GRAPH
        self.graph.view()

