# Open on http://127.0.0.1:5000/nodes_and_edges
# or http://localhost:5000/nodes_and_edges

from os.path import join
from flask import Flask, jsonify  # , abort, make_response

from App.Code.Jira_DF_Reader.jira_df_reader import JiraDFReader
from App.Code.Data_NodesAndEdgesFromDF.create_nodes_and_edges_from_df import NodeAndEdgeCreatorFromDF
from App.Code.Data_Services.service_crossdomain_http_utils import crossdomain
from App.Code.Views_Seaborn.seaborn_analysis import SeabornGenerator

my_source_path = 'C:\\Users\\John\\Documents\\2016\\Python\\JiraStates'
my_csv_file_and_path = join(my_source_path, 'jira_states.csv')

my_jira_df_reader = JiraDFReader(my_csv_file_and_path)
jira_df = my_jira_df_reader.get_final_df()

my_node_and_edge_creator = NodeAndEdgeCreatorFromDF(jira_df)
print(my_node_and_edge_creator)
# jira_df = my_jira_reader.get_jira_df()

node_list = my_node_and_edge_creator.get_unique_node_dict_list()
print('nodes_list = ' + str(node_list))
edge_dict_list = my_node_and_edge_creator.get_unique_combined_edge_dict_list()
print('edges_list = ' + str(edge_dict_list))

my_root_output_path = 'C:\\Users\\John\\Documents\\Visual Studio 2013\\Projects\\DirectedGraph4\\CrosswordViewer'
my_relative_output_path = 'seaborne_images'
my_seaborn_gen = SeabornGenerator(my_root_output_path, my_relative_output_path, jira_df)
# my_output_path = 'C:\\Users\\John\\Documents\\Visual Studio 2013\\Projects\\DirectedGraph4\\CrosswordViewer\\seaborne_images'
# my_seaborn_gen = SeabornGenerator(my_output_path, jira_df)
my_png_list = my_seaborn_gen.get_png_list()
# my_seaborn_gen.open_files_in_chrome(my_dict)
print("my_dict = " + str(my_png_list))

app = Flask(__name__)
@app.route('/nodes_and_edges')
# This is the critical line. It calls crossdomain function which allows the calling app to call it on localhost.
@crossdomain(origin='*')
def node_service():
    return jsonify({'nodes': node_list, 'edges': edge_dict_list, 'pngs': my_png_list})


# @app.route('/todo/api/v1.0/tasks', methods=['GET'])  # all tasks
# def get_tasks():
#     return jsonify({'tasks': tasks})

if __name__ == '__main__':   # Important this needs to be last.
    app.run(debug=True)
