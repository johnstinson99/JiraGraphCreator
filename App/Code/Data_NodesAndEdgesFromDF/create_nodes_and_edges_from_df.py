import pandas as pd
import numpy as np
import json
from collections import OrderedDict

class Node:

    def __init__(self, my_node_name):
        self.node_name = my_node_name
        self.x = 0
        self.y = 0
        self.combined_edges_out = []
        self.combined_edges_in = []
        self.is_primary = False  # primary path is the one with the most commonly followed edges

    def most_popular_edge_out(self):
        # if len(self.combined_edges_out) == 0:
        #     return None
        max_width_0_to_1 = 0
        max_edge = None
        for my_edge in self.combined_edges_out:
            if my_edge.width_0_to_1 > max_width_0_to_1:
                max_width_0_to_1 = my_edge.width_0_to_1
                max_edge = my_edge
        return max_edge

    def as_dict(self):
        return OrderedDict({"node_name": self.node_name,
                            "x": self.x,
                            "y": self.y,
                            "is_primary": self.is_primary})

    def __str__(self):
        return "Node " + self.node_name + " x = " + str(self.x) + ", y = " + str(self.y)

class Edge:

    def __init__(self, my_from_node_object, my_to_node_object):
        self.from_node_object = my_from_node_object
        self.to_node_object = my_to_node_object
        self.nodes = []
        self.is_primary = False
        # print("CREATING EDGE " + str(my_from_node_object) + str(my_to_node_object))

    def __str__(self):
        return self.from_node_object.node_name + ' -> ' + self.to_node_object.node_name + ',\t\t'


class SingleEdge(Edge):

    def __init__(self, my_from_node_object, my_to_node_object, my_day_diff):
        Edge.__init__(self, my_from_node_object, my_to_node_object)
        self.day_diff = my_day_diff

    def __str__(self):
        result = "CombinedEdge: "
        result = Edge.__str__(self)
        result += ' day_diff = ' + str(self.day_diff)
        return result

    def has_same_start_and_end_as(self, other):
        return(self.to_node_object.node_name == other.to_node_object.node_name) \
              & (self.from_node_object.node_name == other.from_node_object.node_name)

    def find_in_combined_edge_list(self, my_combined_edge_list):
        for my_combined_edge in my_combined_edge_list:
            if self.has_same_start_and_end_as(my_combined_edge):
                return my_combined_edge
        return None


class CombinedEdge(Edge):

    def __init__(self, my_from_node_object, my_to_node_object):
        Edge.__init__(self, my_from_node_object, my_to_node_object)
        self.count = 1
        self.width_0_to_1 = 1
        self.day_diff_list = []
        self.day_diff_10_percentile = 0.0
        self.day_diff_50_percentile = 0.0
        self.day_diff_90_percentile = 0.0
        self.day_diff_50_percentile_0_to_1 = 0.0
        my_from_node_object.combined_edges_out.append(self)
        my_to_node_object.combined_edges_in.append(self)

    def __str__(self):
        return "CombinedEdge: " + \
            Edge.__str__(self) + \
            ' day_diff_list = ' + str(self.day_diff_list) + \
            ' count = ' + str(self.count) + \
            ' width = ' + str(self.width_0_to_1) + \
            ', day_diff_50_percentile = ' + str(self.day_diff_50_percentile) + \
            ', day_diff_50_percentile_0_to_1 = ' + str(self.day_diff_50_percentile_0_to_1)

    def calc_percentile_day_diffs(self):
        a = np.array(self.day_diff_list)
        self.day_diff_10_percentile = np.percentile(a, 10)
        self.day_diff_50_percentile = np.percentile(a, 50)
        self.day_diff_90_percentile = np.percentile(a, 90)

    def as_list(self):
        return [self.from_node_object.node_name, self.to_node_object.node_name, self.width_0_to_1, self.day_diff_50_percentile_0_to_1, self.day_diff_10_percentile, self.day_diff_50_percentile, self.day_diff_90_percentile]

    def as_dict(self):
        return OrderedDict({"from": self.from_node_object.node_name,
                "to": self.to_node_object.node_name,
                "width_0_to_1": self.width_0_to_1,
                "day_diff_50_percentile_0_to_1": self.day_diff_50_percentile_0_to_1,
                "day_diff_10_percentile": self.day_diff_10_percentile,
                "day_diff_50_percentile": self.day_diff_50_percentile,
                "day_diff_90_percentile": self.day_diff_90_percentile,
                "is_primary": self.is_primary})

class NodeAndEdgeCreatorFromDF:

    def __init__(self, my_jira_df):
        self.jira_df = my_jira_df
        max_x = 1000
        max_y = 500
        # self.file_and_path_string = my_file_and_path_string
        # self.jira_df = pd.read_csv(my_file_and_path_string)
        self.issue_list = pd.Series.unique(self.jira_df['IssueNo'])
        # self.unique_node_list = list(pd.Series.unique(self.jira_df['To']))
        self.unique_node_dict = {node_name: Node(node_name) for node_name in pd.Series.unique(self.jira_df['To'])}
        # self.set_unique_node_x_y_coords(self.unique_node_dict.values())
        edge_df = self.jira_df[['From', 'To', 'DayDiff']]
        single_edge_list = [SingleEdge(self.unique_node_dict[row[0]],
                                       self.unique_node_dict[row[1]],
                                       row[2])
                                 for row in edge_df.values
                                 if row[0] != 'Undefined']
        self.unique_combined_edge_object_list = \
            self.create_unique_combined_edge_object_list(single_edge_list)
        self.max_edge_count = 0
        self.max_day_diff_50_percentile = 0.0
        self.calc_line_widths_and_50_percentile_day_diffs()
        primary_path_node_edge_tuple = self.calc_primary_node_path_list(self.unique_node_dict)
        self.primary_path_node_list = primary_path_node_edge_tuple[0]
        self.primary_path_edge_list = self.calc_primary_path_edges()
        self.primary_path_edge_list = primary_path_node_edge_tuple[1]
        self.secondary_nodes = self.find_secondary_nodes(
                list(self.unique_node_dict.values()),
                self.primary_path_node_list)
        self.set_primary_node_x_y_postions(self.primary_path_node_list, self.primary_path_edge_list, max_x, max_y)
        self.calc_secondary_node_positions(self.secondary_nodes, max_x, max_y)

    def get_jira_df(self):
        return self.jira_df

    def tuple_mean(self, my_tuple_list):
        if len(my_tuple_list) == 0:
            return (0, 0)
        unzipped_list = list(zip(*my_tuple_list))
        x_list = unzipped_list[0]
        y_list = unzipped_list[1]
        return (sum(x_list)/len(x_list), sum(y_list)/len(y_list))

    def calc_secondary_node_positions(self, my_secondary_nodes, max_x, maxy):
        # print("CALCING SECONDARY NODE POSITIONS")
        for my_node in my_secondary_nodes:
            # print(str(my_node))
            from_edges = my_node.combined_edges_in
            for my_edge in from_edges:
                print(str(my_edge))
            from_nodes_x_y_tuple_list = list([(from_edge.from_node_object.x, from_edge.from_node_object.y)
                                         for from_edge in from_edges])
            # print (str(from_nodes_y))
            from_nodes_x_y_mean_tuple = self.tuple_mean(from_nodes_x_y_tuple_list)

            my_node.y = from_nodes_x_y_mean_tuple[1]
            to_edges = my_node.combined_edges_out
            to_nodes_x_y_tuple_list = list([(to_edge.to_node_object.x, to_edge.to_node_object.y)
                                       for to_edge in to_edges])
            to_nodes_x_y_mean_tuple = self.tuple_mean(to_nodes_x_y_tuple_list)
            my_node.x = to_nodes_x_y_mean_tuple[0]
            if my_node.y == 0:
                my_node.y = to_nodes_x_y_mean_tuple[1] + max_y/10
            if my_node.x == 0:
                my_node.x = from_nodes_x_y_mean_tuple[0] + max_x/10

    def calc_primary_path_edges(self):
        edge_list = []
        for my_node in self.primary_path_node_list:
            edge_list += my_node.combined_edges_out
        return edge_list

    def find_secondary_nodes(self, unique_nodes, primary_path_nodes):
        # return all nodes in unique_nodes that aren't in primary_path_nodes
        print(str(unique_nodes))
        print(str(primary_path_nodes))
        unique_node_set = set(unique_nodes)
        primary_path_node_set = set(primary_path_nodes)
        difference_set = unique_node_set.difference(primary_path_node_set)
        return list(difference_set)

    def calc_primary_node_path_list(self, my_unique_node_dict):
        start_node = my_unique_node_dict["Open"]  # throws exception if not there.
        start_node.is_primary = True
        print("start_node = " + start_node.node_name)
        primary_node_list = [start_node]
        primary_edge_list = []
        self.get_next_popular_node_and_edge(
                start_node,
                primary_node_list,
                primary_edge_list)
        print("PRIMARY_NODE_LIST")
        print(str(primary_node_list))
        print("PRIMARY_EDGE_LIST")
        print(str(primary_edge_list))
        return (primary_node_list, primary_edge_list)

    def get_next_popular_node_and_edge(self, current_node, partial_primary_node_list, partial_primary_edge_list):
        if len(current_node.combined_edges_out) == 0:
            return
        next_edge = current_node.most_popular_edge_out()
        next_edge.is_primary = True
        # print("next_max_edge = " + str(next_max_edge))
        next_node = next_edge.to_node_object
        next_node.is_primary = True
        # print("next_node = " + next_node.node_name)
        partial_primary_node_list.append(next_node)
        partial_primary_edge_list.append(next_edge)
        self.get_next_popular_node_and_edge(
                next_node,
                partial_primary_node_list,
                partial_primary_edge_list)


    '''def set_primary_node_x_y_postions_0_to_n(self, my_primary_nodes, my_max_x, my_max_y):
        no_of_nodes = len(my_primary_nodes)
        no_of_spaces = no_of_nodes + 1
        x_space_between  = my_max_x/no_of_spaces
        y_space_between = my_max_y/no_of_spaces
        x = x_space_between/2
        y = y_space_between/2
        for my_node in my_primary_nodes:
            my_node.x = x
            my_node.y = y
            x += x_space_between
            y += y_space_between'''

    def set_primary_node_x_y_postions(self, my_primary_nodes, my_primary_edges, my_max_x, my_max_y):
        print("MY_PRJMARY_NODES = " + str(my_primary_nodes))
        sum_of_median_days_0_to_1 = 0
        for my_edge in my_primary_edges:
            sum_of_median_days_0_to_1 += my_edge.day_diff_50_percentile_0_to_1
        length_list_which_sums_to_1 = [my_edge.day_diff_50_percentile_0_to_1/sum_of_median_days_0_to_1
                       for my_edge in my_primary_edges]

        # Find start position and max position
        no_of_nodes = len(my_primary_nodes)
        no_of_spaces = no_of_nodes + 1
        average_x_space_between  = my_max_x/no_of_spaces
        average_y_space_between = my_max_y/no_of_spaces
        start_x = average_x_space_between/2
        start_y = average_y_space_between/2
        available_x = my_max_x - average_x_space_between
        available_y = my_max_y - average_y_space_between
        position_tuple_list = [(start_x, start_y)]
        previous_x = start_x
        previous_y = start_y
        for my_length_which_sums_to_1 in length_list_which_sums_to_1:
            x_diff = my_length_which_sums_to_1 * available_x
            y_diff = my_length_which_sums_to_1 * available_y
            previous_x += x_diff
            previous_y += y_diff
            position_tuple_list.append((previous_x, previous_y))
        print("POSITION_TUPLE_LIST = ")
        print(str(position_tuple_list))
        print("MY_PRJMARY_NODES = " + str(my_primary_nodes))
        for i in range(0, len(my_primary_nodes)):
            my_primary_nodes[i].x = position_tuple_list[i][0]
            my_primary_nodes[i].y = position_tuple_list[i][1]

    def set_secondary_node_x_y_positions(self):
        '''X = place between outs, Y = place between ins.
        If two states have same ins and outs, move them vertically.
        Use dotted lines to connect non critical path items, to indicate the length doesn’t represent number of days.
        Pass the dotted line fact in the API.'''


    '''def set_unique_node_x_y_coords(self, my_unique_node_list):
        # TODO replace later with algorithm using a Python graphing library.
        my_x = 100
        my_y = 100
        for my_node in my_unique_node_list:
            my_node.x = my_x
            my_node.y = my_y
            my_x += 100'''

    def get_unique_node_object(self):
        return list(self.unique_node_dict.values())

    def get_unique_node_dict_list(self):
        node_dict = [my_node.as_dict() for my_node in self.unique_node_dict.values()]
        # print('edge_list = ' + str(edge_list))
        return node_dict

    def get_unique_combined_edge_list(self):
        edge_list = [my_edge.as_list() for my_edge in self.unique_combined_edge_object_list]
        # print('edge_list = ' + str(edge_list))
        return edge_list

    def get_unique_combined_edge_dict_list(self):
        edge_dict = [my_edge.as_dict() for my_edge in self.unique_combined_edge_object_list]
        # print('edge_list = ' + str(edge_list))
        return edge_dict

    def create_unique_combined_edge_object_list(self, my_single_edge_list):
        my_unique_combined_edge_object_list = []
        for my_single_edge in my_single_edge_list:
            my_combined_edge = my_single_edge.find_in_combined_edge_list(my_unique_combined_edge_object_list)
            if my_combined_edge is None:
                my_combined_edge = CombinedEdge(
                        my_single_edge.from_node_object,
                        my_single_edge.to_node_object)
                my_unique_combined_edge_object_list.append(my_combined_edge)
            else:
                my_combined_edge.count += 1
            my_combined_edge.day_diff_list.append(my_single_edge.day_diff)
        return my_unique_combined_edge_object_list

    def calc_line_widths_and_50_percentile_day_diffs(self):
        for my_combined_edge in self.unique_combined_edge_object_list:
            if my_combined_edge.count > self.max_edge_count:
                self.max_edge_count = my_combined_edge.count
            my_combined_edge.calc_percentile_day_diffs()

            for my_combined_edge in self.unique_combined_edge_object_list:
                my_combined_edge.width_0_to_1 = my_combined_edge.count / self.max_edge_count
                if my_combined_edge.day_diff_50_percentile > self.max_day_diff_50_percentile:
                    self.max_day_diff_50_percentile = my_combined_edge.day_diff_50_percentile

            for my_combined_edge in self.unique_combined_edge_object_list:
                my_combined_edge.day_diff_50_percentile_0_to_1 = \
                    my_combined_edge.day_diff_50_percentile/self.max_day_diff_50_percentile

    def __str__(self):
        str1 = 'df = \n' + str(self.jira_df) + '\n'
        str2 = 'issue_list = ' + str(self.issue_list) + '\n'
        str3 = 'state_list = ' + str(self.unique_node_dict.keys()) + '\n'
        # str4 = 'edge_tuple_set = ' + str(self.edge_tuple_set) + '\n'
        # str4 = '\nedge_object_list = \n'
        # for my_edge in self.single_edge_list:
        #     str4 += '\t' + str(my_edge) + '\n'
        str5 = '\nunique_edge_object_list = \n'
        for my_edge in self.unique_combined_edge_object_list:
            str5 += '\t' + str(my_edge) + '\n'
        str6 = '\nunique_node_objects\n'
        for my_node in self.unique_node_dict.values():
            str6 += '\t' + my_node.node_name + '\n'
            str6 += '\t\tedges_out = '
            str6 += '\t' + str([str(my_node) for my_node in my_node.combined_edges_out]) +'\n'
            str6 += '\t\tedges_in = '
            str6 += '\t' + str([str(my_edge) for my_edge in my_node.combined_edges_in]) +'\n'
        str7 = "non_primary_nodes\n"
        for my_node in self.secondary_nodes:
            str7 += "\t" + my_node.node_name + "\n"

        return str1 + str2 + str3 + str5 + str6 + str7


