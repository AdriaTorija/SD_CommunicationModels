from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process, Lock
import worker as w
server = SimpleXMLRPCServer(("localhost",8000),allow_none=True)

from redis import Redis
import json
r = Redis()
lock = Lock()
server.register_introspection_functions()
WORKERS = {}
WORKER_ID=0

def start_worker(id):
    print("Starting Worker: ", id)
    
    while True:
        #See if there are tasks to be done
        task_object = r.blpop(['Task'], 30)
        if(task_object != None):
            task = json.loads(task_object[1])
            funct = task["Function"]
            param = task["Parameter"]

            #Execute the function according to the parameter
            if funct == "counting_words":
                result = w.counting_words(param)
                print("WORKER ID: " + str(id) + " Result:" + str(result))
                save_result(result)

            elif funct == "word_count":
                result = str(w.word_count(param))
                print("WORKER ID: " + str(id) + " Result:" + result)
                save_result(result)

#Saves the result of the function
def save_result(result):
    lock.acquire()
    #
    #
    #
    #S'haura de canviar el nom de la cua depenen de la tasca
    #
    #
    #
    r.rpush('fi', result)
    lock.release()

#Create a task
def create_task(func, params):
    #
    #
    #
    #S'haura d'afegir nous parametres per el multiple task
    #
    #
    #
    print("Creating a new task...")
    print("Function: " + func)
    print("Parameter: " +params)
    dades = {
        'Function': func,
        'Parameter': params
    }

    #Save the json object to the redis 'Task' queue
    r.rpush('Task', json.dumps(dades))

#Create a worker
def create_worker():
    global WORKERS
    global WORKER_ID
    proc = Process(target=start_worker,args=(WORKER_ID,))
    proc.start()
    WORKERS[WORKER_ID] = proc
    WORKER_ID += 1

#Delete a worker
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
server.register_function(create_task,"create_task")

try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print("Bye Bye...")