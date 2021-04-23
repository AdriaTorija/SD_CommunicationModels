from xmlrpc.server import SimpleXMLRPCServer
from multiprocessing import Process
import worker as w
server = SimpleXMLRPCServer(("localhost",8000),allow_none=True)

from redis import Redis
import json

r = Redis()
server.register_introspection_functions()
WORKERS = {}
WORKER_ID=0
TASK_ID=0

def start_worker(id):
    print("----------\nStarting Worker: " + str(id))
    
    while True:
        #See if there are tasks to be done
        task_object = r.blpop(['Task'], 30)
        if(task_object != None):
            task = json.loads(task_object[1])
            funct = task["Function"]
            param = task["Parameter"]
            t_id = task["Task_ID"]

            if(funct != "create_result"):
                method = getattr(w, funct)
                result = method(param)
                print("----------\nWORKER_ID: " + str(id) + "\nTask_ID: " + str(t_id) + "\nParam: " + param + "\nResult:" + str(result) + "\n")
                r.rpush('Task' + str(t_id), json.dumps(result))
            else:
                last = task["Last_funct"]
                create_result(t_id, last, param)


def create_result(t_id, funct, param):

    queue_name = 'Task' + str(t_id)

    #Wait for all the results
    length = r.llen(queue_name)
    while param > length:
        length = r.llen(queue_name)
    
    i = 0
    
    #Counting Words
    if funct == "counting_words":
        final = 0

        while i < param:
            jsonRes = r.lpop(queue_name)
            res = json.loads(jsonRes)
            final = int(res) + final
            i += 1

    #Word Count
    elif funct == "word_count":
        final = dict()
        
        while i < param:
            jsonRes = r.lpop(queue_name)
            res_dict = json.loads(jsonRes)
            
            for x in res_dict:
                if x in final:
                    final[x] += res_dict[x]
                else:
                    final[x] = res_dict[x]
    
            i += 1

    #Final result -> Client
    print("\n----------\nTask_ID: " + str(t_id) + "\nFinal result:" + str(final) + "\n")

    result = {
            'Task_ID': t_id,
            'Result': final
        }

    r.rpush('Result', json.dumps(result))

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

#Create a worker
def create_worker():
    print("----------\nSERVER: CREATE_WORKER")
    global WORKERS
    global WORKER_ID
    proc = Process(target=start_worker,args=(WORKER_ID,))
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