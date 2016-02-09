# Open on http://127.0.0.1:5000/nodes
# or http://localhost:5000/nodes
# or http://localhost:5000/edges
from os.path import join
from App.Code.JiraToGraph.jira_graph_creator import JiraReader
from flask import Flask, jsonify  # , abort, make_response
from App.Code.JiraToGraph.service_crossdomain_http_utils import crossdomain


my_dir = 'C:\\Users\\John\\Documents\\2016\\Python\\JiraStates'
f = join(my_dir, 'jira_states.csv')

my_jira_reader = JiraReader(f)
print(my_jira_reader)

nodes_list = my_jira_reader.get_unique_node_list()
print('nodes_list = ' + str(nodes_list))
edges_list = my_jira_reader.get_unique_combined_edge_list()
print('edges_list = ' + str(edges_list))


app = Flask(__name__)
@app.route('/nodes')
# This is the critical line. It calls crossdomain function which allows the calling app to call it on localhost.
@crossdomain(origin='*')
def node_service():
    return jsonify({'nodes': nodes_list})

@app.route('/edges')
# This is the critical line. It calls crossdomain function which allows the calling app to call it on localhost.
@crossdomain(origin='*')
def edge_service():
    return jsonify({'nodes': edges_list})


# @app.route('/todo/api/v1.0/tasks', methods=['GET'])  # all tasks
# def get_tasks():
#     return jsonify({'tasks': tasks})

if __name__ == '__main__':   # Important this needs to be last.
    app.run(debug=True)
