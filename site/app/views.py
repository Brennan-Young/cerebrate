import json
from time import time
from random import random
from flask import Flask, render_template, make_response
from flask_socketio import SocketIO, emit
import rethinkdb as r

from app import app

# app = Flask(__name__)
socketio = SocketIO(app)

def dbBackground():
    r.connect( "35.163.48.63", 28015, db = "test").repl()
    # r.table("demandTest").changes().run()
    # cursor = r.table("demandTest").order_by(index="timeStamp").filter(r.row["nodeID"] == 0).changes().run()
    cursor = r.table("demandTest").filter(r.row["nodeID"] == 0).changes().run()
    print('three')
    return cursor
    # for document in cursor:
    #     socketio.emit('components', {'data': cc}, json=True)
    #     socketio.sleep(0.169)

def dbSupply():
    r.connect( "35.163.48.63", 28015, db = "test").repl()
    # r.table("supplyCount").changes().run()
    cursor = r.table("supplyCount").filter(r.row["nodeID"] == 0).changes().run()
    return cursor

thread = None

@socketio.on('connect')
def connected():
    print('connected')
    global thread
    if thread is None:
        thread = socketio.start_background_task(target = dbBackground)

@socketio.on('disconnect')
def disconnected():
    print('disconnected')    

@app.route('/')
def hello_world():
    return render_template('index.html', data='test')

# @app.route('/live-graph')
# def live_graph():
#     with open('networkGraph.txt','r') as f:
#         testData = json.load(f)
#     response2 = make_response(json.dumps(testData))
#     response2.content_type = 'application/json'
#     print("hello_world")
#     return response2

@app.route('/supply-data')
def supply_data():
    cursor = dbSupply()
    print('a')
    for document in cursor:
        x = document["new_val"]
        data = [float(x["timeStamp"]), float(x["supply"])]
        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        break
    return response

@app.route('/live-data')
def live_data():
    # Create a PHP array and echo it as JSON
    # data = [time() * 1000, random() * 100]
    # print(data)
    #for document in cursor:
     #   data = [(document["timeStamp"],document["requestCount"])]
    cursor = dbBackground()
    for document in cursor:
        # print(document)
    	x = document["new_val"]
        data = [float(x["timeStamp"]),float(x["requestCount"])]
    
        print(data)
        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        print("I did it")
        break
    return response

# @app.route('/live-data2')

# if __name__ == '__main__':
#     app.run(debug=False, host='0.0.0.0', port=5000)
