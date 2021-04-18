from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process
import worker as w
server = SimpleXMLRPCServer(("localhost",8000),allow_none=True)


from flask import Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Web Created"
app.run(port=8080)




server.register_introspection_functions()
WORKERS = {}
WORKER_ID=0

def start_worker(id, file):
    print("Starting Worker: ", id)
    

def work(func, params):
    print("Doing Some Work")


def create_worker():
    global WORKERS
    global WORKER_ID
    proc = Process(target=start_worker,args=(WORKER_ID, 'prova.txt'))
    proc.start()
    WORKERS[WORKER_ID] = proc
    WORKER_ID += 1


def delete_worker(id):
    global WORKERS
    try:
        WORKERS[id].terminate()
        del WORKERS[id]
        print("Worker ",id," Deleted")
    except Exception:
        print("Worker not found")
    
def list_workers():
    return str(WORKERS.items())

server.register_function(create_worker,"create_worker")
server.register_function(delete_worker,"delete_worker")
server.register_function(list_workers,"list_workers")

try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print("Bye Bye...")