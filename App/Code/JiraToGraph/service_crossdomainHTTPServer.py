# Open on http://127.0.0.1:5000/my_service
# or http://localhost:5000/my_service

from flask import Flask, jsonify  # , abort, make_response
from App.Code.JiraToGraph.service_crossdomain_http_utils import crossdomain

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Clear Shed',
        'description': u'Get rid of sawdust',
        'done': False
    },
    {
        'id': 2,
        'title': u'Mend pipe',
        'description': u'Solder it',
        'done': False
    }
]


@app.route('/my_service')
# This is the critical line. It calls crossdomain function which allows the calling app to call it on localhost.
@crossdomain(origin='*')
def my_service():
    return jsonify({'tasks': tasks})

# @app.route('/todo/api/v1.0/tasks', methods=['GET'])  # all tasks
# def get_tasks():
#     return jsonify({'tasks': tasks})

if __name__ == '__main__':   # Important this needs to be last.
    app.run(debug=True)
