import json
import urllib.request

#Start worker
def start_worker(id,r):
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
                method = globals()[funct]
                #method = getattr(w, funct)
                result = method(param)
                print("----------\nWORKER_ID: " + str(id) + "\nTask_ID: " + str(t_id) + "\nParam: " + param + "\nResult:" + str(result) + "\n")
                r.rpush('Task' + str(t_id), json.dumps(result))
            else:
                last = task["Last_funct"]
                create_result(t_id, last, param, r)


#Create the final result of the Task
def create_result(t_id, funct, param, r):

    queue_name = 'Task' + str(t_id)
    funct = 'res_' + funct

    #Wait for all the results
    length = r.llen(queue_name)
    while param > length:
        length = r.llen(queue_name)

    method = globals()[funct]
    #method = getattr(w, funct)
    method_res = method(queue_name, param, r)
        
    #Final result -> Client
    print("\n----------\nTask_ID: " + str(t_id) + "\nFinal result:" + str(method_res) + "\n")

    task_res = {
            'Task_ID': t_id,
            'Result': method_res
        }

    r.rpush('Result', json.dumps(task_res))


#Method to read a file
def read_file(file):
    try:
        #f = open(file,'r') 
        #lines=f.read()
        #f.close
        f = urllib.request.urlopen(file).read().decode('utf-8')
        return f
    except EOFError:
        print("Error there is no file")   


#Count how many words are in a file
def counting_words(file):
    return len(read_file(file).split())


#Count how many times a word appears in a file
def word_count(file):
    counts= dict()
    lines=read_file(file)
    words = lines.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


#Get the final result of the Task counting_words
def res_counting_words(queue_name, param, r):
    final = 0
    i = 0
    while i < param:
        jsonRes = r.lpop(queue_name)
        res = json.loads(jsonRes)
        final = int(res) + final
        i += 1
    
    return final


#Get the final result of the Task word_count
def res_word_count(queue_name, param, r):
    final = dict()
    i = 0

    while i < param:
        jsonRes = r.lpop(queue_name)
        res_dict = json.loads(jsonRes)
            
        for x in res_dict:
            if x in final:
                final[x] += res_dict[x]
            else:
                final[x] = res_dict[x]
    
        i += 1

    return final