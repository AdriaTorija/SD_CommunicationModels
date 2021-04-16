WORKERS = {}
WORKER_ID = 0

def start_worker()




def create_worker()
    global WORKERS
    global WORKER_ID

    proc = Process(target=start_worker, args=(WORKER_ID,))
    proc.start()
    WORKERS[WORKER_ID] = proc
    
    
    
    WORKER_ID += 1