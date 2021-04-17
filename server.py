from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process
import worker as w
server = SimpleXMLRPCServer(("localhost",8000),allow_none=True)
server.register_introspection_functions()
WORKERS = {}
WORKER_ID=0


def start_worker(id):
    print("Starting Worker: ", id)

def work(func, params):
    print("Doing Some Work")


def create_worker():
    global WORKERS
    global WORKER_ID
    proc = Process(target=start_worker,args=(WORKER_ID,))
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
    global WORKERS
    global WORKER_ID
    i=0
    llista = '{'
    while i < WORKER_ID:
        llista = llista + str(i) + ','
        i += 1
    llista = llista + '}'
    return str(WORKERS.items())

server.register_function(create_worker,"create_worker")
server.register_function(delete_worker,"delete_worker")
server.register_function(list_workers,"list_workers")

try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print("Bye Bye...")