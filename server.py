from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process
import worker as w
from redis import Redis
import json

server = SimpleXMLRPCServer(("localhost",8001),allow_none=True)
r = Redis()
server.register_introspection_functions()
WORKERS = {}
WORKER_ID=0
TASK_ID=0

#Create a worker
def create_worker():
    print("----------\nSERVER: CREATE_WORKER")
    global WORKERS
    global WORKER_ID
    proc = Process(target=w.start_worker,args=(WORKER_ID,r,))
    proc.start()
    WORKERS[WORKER_ID] = proc
    WORKER_ID += 1


#Delete a worker
def delete_worker(id):
    print("----------\nSERVER: DELETE_WORKER")
    global WORKERS
    try:
        WORKERS[id].terminate()
        del WORKERS[id]
        print("Worker ",id," Deleted")
    except Exception:
        print("SERVER: [ERROR] WORKER NOT FOUND")


#List all workers
def list_workers():
    print("SERVER: LIST_WORKERS")
    elem = WORKERS.items()

    if len(elem) == 0:
        string = 'No workers found'
    else:
        string = ''
        for id, proces in elem:
            string = string + "WORKER ID: " + str(id) + " " + str(proces) + "\n"
        
    return string


#Create a task
def create_task(func, params):
    print("----------\nSERVER: CREATE_TASK")
    global TASK_ID

    for p in params:

        print("----------\nSERVER: Creating a new task..." + "\n\tTask_ID: " + str(TASK_ID) + "\n\tFunction: " + func + "\n\tParameter: " + p + "\n")

        task = {
            'Task_ID': TASK_ID,
            'Function': func,
            'Parameter': p
        }
        
        #Save the json object to the redis 'Task' queue
        r.rpush('Task', json.dumps(task))

    task = {
        'Task_ID': TASK_ID,
        'Function': "create_result",
        'Parameter': len(params),
        'Last_funct': func
    }
    r.rpush('Task', json.dumps(task))

    TASK_ID += 1


#Get all the results
def get_result():
    print("----------\nSERVER: GET_RESULT")
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