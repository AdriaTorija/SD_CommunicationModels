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
TASK_ID=0

def start_worker(id):
    print("Starting Worker: ", id)
    
    while True:
        #See if there are tasks to be done
        task_object = r.blpop(['Task'], 30)
        if(task_object != None):
            task = json.loads(task_object[1])
            funct = task["Function"]
            param = task["Parameter"]
            t_id = task["Task_ID"]

            #Execute the function according to the parameter
            if funct == "counting_words":
                result = w.counting_words(param)
                print("WORKER ID: " + str(id) + " TASK ID: " + str(t_id) + " Result:" + str(result))
                save_result(t_id, result)

            elif funct == "word_count":
                result = str(w.word_count(param))
                print("WORKER ID: " + str(id) + " TASK ID: " + str(t_id) + " Result:" + result)
                save_result(t_id, result)
            
            elif funct == "juntar_resultat":
                print("Estic juntant!")
                last = task["Last_funct"]
                create_result(t_id, last, param)


def create_result(t_id, funct, param):

    queue_name = 'Task' + str(t_id)

    #Wait for all the results
    length = r.llen(queue_name)
    while param > length:
        length = r.llen(queue_name)

    if funct == "counting_words":
        final = 0
        i = 0
        while i < param:
            x = r.lpop(queue_name).decode("utf-8")
            final = int(x) + final
            i += 1

        print("Resultat final: " + str(final))

        result = {
            'Task_ID': t_id,
            'Result': final
        }

        r.rpush('Result', json.dumps(result))


    elif funct == "word_count":
        print("Word")
        
#Get all the results
def get_result():
    all_results = r.lrange('Result', 0, -1)

    if len(all_results) == 0:
        string = "No results found"
    else:
        string = ''

        for result in all_results:
            json_result = json.loads(result)
            t_id = json_result['Task_ID']
            res = json_result['Result']
            string = string + 'Task_ID: ' + str(t_id) + ' Result: ' + str(res) + '\n' 

    return string

#Saves the result of the function
def save_result(t_id, result):
    lock.acquire()
    r.rpush('Task' + str(t_id), result)
    lock.release()

#Create a task
def create_task(func, params):
    global TASK_ID

    for p in params:

        print("Creating a new task...")
        print("Task_ID: " + str(TASK_ID))
        print("Function: " + func)
        print("Parameter: " + p)
        print()

        task = {
            'Task_ID': TASK_ID,
            'Function': func,
            'Parameter': p
        }
        
        #Save the json object to the redis 'Task' queue
        r.rpush('Task', json.dumps(task))

    task = {
        'Task_ID': TASK_ID,
        'Function': "juntar_resultat",
        'Parameter': len(params),
        'Last_funct': func
    }
    r.rpush('Task', json.dumps(task))

    TASK_ID += 1

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
server.register_function(get_result,"get_result")

try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt:
    print("Bye Bye...")