from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process
import worker as w
server = SimpleXMLRPCServer(("localhost",8000),allow_none=True)

WORKERS = {}
WORKER_ID=0
print("Lokooo")


def start_worker(id):
    i = 0
    while 0 < 1:
        i+=1
    return 12

def create_worker():
    global WORKERS
    global WORKER_ID
    proc = Process(target=start_worker,args=(WORKER_ID,))
    proc.start()
    WORKERS[WORKER_ID] = proc
    WORKER_ID += 1


def delete_worker(id):
    global WORKERS
    WORKERS[id].terminate()
    del WORKERS[id]
    print("Worker Deleted")

def list_workers():
    i=0
    llista = '{'
    while i < WORKER_ID:
        llista = llista + str(i) + ','
        i += 1
    llista = llista + '}'
    return str(WORKERS.items())

server.register_function(create_worker,"create_worker")
server.register_function(delete_worker,"delete_worker")


try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print("Bye Bye...")