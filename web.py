from flask import Flask, render_template
from flask_socketio import SocketIO
import rethinkdb as r

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')

def getRethinkTable():    
    r.connect( "35.163.48.63", 28015, db = "test").repl()
    cursor = r.table("demandTest").run()
    for document in cursor:
    	print(document)
        socketio.emit('components', {'data': document}, json = True)
        socketio.sleep(0.1)

thread = None
@socketio.on('connect')
def connected():
    print('connected')
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=getRethinkTable)

@socketio.on('disconnect')
def disconnected():
    print('disconnected')    
    
@app.route('/')
def hello():
    return render_template("main.html")

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')