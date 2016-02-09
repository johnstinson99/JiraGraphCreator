import pandas as pd
import numpy as np
import json


class Edge:

    def __init__(self, my_from_string, my_to_string):
        self.from_string = my_from_string
        self.to_string = my_to_string

    def __str__(self):
        return self.from_string + ' -> ' + self.to_string + ',\t\t'


class SingleEdge(Edge):

    def __init__(self, my_from_string, my_to_string, my_day_diff):
        Edge.__init__(self, my_from_string, my_to_string)
        self.day_diff = my_day_diff

    def __str__(self):
        result = "CombinedEdge: "
        result = Edge.__str__(self)
        result += ' day_diff = ' + str(self.day_diff)
        return result

    def has_same_start_and_end_as(self, other):
        return(self.to_string == other.to_string) & (self.from_string == other.from_string)

    def find_in_combined_edge_list(self, my_combined_edge_list):
        for my_combined_edge in my_combined_edge_list:
            if self.has_same_start_and_end_as(my_combined_edge):
                return my_combined_edge
        return None


class CombinedEdge(Edge):

    def __init__(self, my_from_string, my_to_string):
        Edge.__init__(self, my_from_string, my_to_string)
        self.count = 1
        self.width_0_to_1 = 1
        self.day_diff_list = []
        self.day_diff_10_percentile = 0.0
        self.day_diff_50_percentile = 0.0
        self.day_diff_90_percentile = 0.0
        self.day_diff_50_percentile_0_to_1 = 0.0

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
        return [self.from_string, self.to_string, self.width_0_to_1, self.day_diff_50_percentile_0_to_1, self.day_diff_10_percentile, self.day_diff_50_percentile, self.day_diff_90_percentile]

class JiraReader:

    def __init__(self, my_file_and_path_string):
        self.file_and_path_string = my_file_and_path_string
        self.jira_df = pd.read_csv(my_file_and_path_string)
        self.issue_list = pd.Series.unique(self.jira_df['IssueNo'])
        self.unique_node_list = list(pd.Series.unique(self.jira_df['To']))
        edge_df = self.jira_df[['From', 'To', 'DayDiff']]
        self.single_edge_list = [SingleEdge(row[0], row[1], row[2]) for row in edge_df.values if row[0] != 'Undefined']
        self.unique_combined_edge_list = []
        self.populate_unique_combined_edge_list()
        self.max_edge_count = 0
        self.max_day_diff_50_percentile = 0.0
        self.calc_line_widths_and_50_percentile_day_diffs()

    def get_unique_node_list(self):
        return self.unique_node_list

    def get_unique_combined_edge_list(self):
        edge_list = [my_edge.as_list() for my_edge in self.unique_combined_edge_list]
        # print('edge_list = ' + str(edge_list))
        return edge_list

    def populate_unique_combined_edge_list(self):
        for my_single_edge in self.single_edge_list:
            my_combined_edge = my_single_edge.find_in_combined_edge_list(self.unique_combined_edge_list)
            if my_combined_edge is None:
                my_combined_edge = CombinedEdge(my_single_edge.from_string, my_single_edge.to_string)
                self.unique_combined_edge_list.append(my_combined_edge)
            else:
                my_combined_edge.count += 1
            my_combined_edge.day_diff_list.append(my_single_edge.day_diff)

    def calc_line_widths_and_50_percentile_day_diffs(self):
        for my_combined_edge in self.unique_combined_edge_list:
            if my_combined_edge.count > self.max_edge_count:
                self.max_edge_count = my_combined_edge.count
            my_combined_edge.calc_percentile_day_diffs()

            for my_combined_edge in self.unique_combined_edge_list:
                my_combined_edge.width_0_to_1 = my_combined_edge.count / self.max_edge_count
                if my_combined_edge.day_diff_50_percentile > self.max_day_diff_50_percentile:
                    self.max_day_diff_50_percentile = my_combined_edge.day_diff_50_percentile

            for my_combined_edge in self.unique_combined_edge_list:
                my_combined_edge.day_diff_50_percentile_0_to_1 = \
                    my_combined_edge.day_diff_50_percentile/self.max_day_diff_50_percentile

    def __str__(self):
        str1 = 'df = \n' + str(self.jira_df) + '\n'
        str2 = 'issue_list = ' + str(self.issue_list) + '\n'
        str3 = 'state_list = ' + str(self.unique_node_list) + '\n'
        # str4 = 'edge_tuple_set = ' + str(self.edge_tuple_set) + '\n'
        str4 = '\nedge_object_list = \n'
        for my_edge in self.single_edge_list:
            str4 += '\t' + str(my_edge) + '\n'
        str5 = '\nunique_edge_object_list = \n'
        for my_edge in self.unique_combined_edge_list:
            str5 += '\t' + str(my_edge) + '\n'
        return str1 + str2 + str3 + str4 + str5


