from random import randint, sample, random
from time import sleep
from os import system

class Resource:
    def __init__(self, id, time):
        self.id = id
        self.__time = time    
    
    def time(self):
        return self.__time
    
    def decrement(self):
        self.__time -= 1
    
    def is_done(self):
        result = self.__time <= 0
        if result:
            self.__time = 0
        return result
    
    def __repr__(self):
        return 'R%d, Time: (%d s)' % (self.id, self.__time) if not self.is_done() else 'R%d Complete!' % self.id
    
class User:
    def __init__(self, id):
        self.id = id
        self.__res_list = []
    
    def is_complete(self):
        return not self.curr_req()
    
    def req_list(self):
        return self.__res_list
    
    def res_request(self, l):
        self.__res_list = l
    
    def show_req(self):
        return [str(req) for req in self.__res_list]
        
    def curr_req(self):
        for res in self.__res_list:
            if not res.is_done():
                return res
        return None

    def display(self):
        return 'U%d\n|-- Requests: ' % self.id + '{0}'.format(self.__res_list) if len(self.__res_list) > 0 else ''

    def __repr__(self):
        return 'U%d' % self.id

class Queue:
    def __init__(self, res_list):
        self.__queue = {res: [] for res in res_list}
    
    def queue(self):
        return self.__queue
    
    def enqueue(self, process, curr_res, curr_user):
        time_left = 0
        last_item = self.last_queue(curr_res.id)
        if last_item:
            last_item_key, last_item_value = next(iter(last_item.items()))
            time_left += last_item_value.time()
            time_left += last_item_key.curr_req().time()
        else: # If no users are in queue
            for (_, res) in process.items():
                if curr_res.id == res.id:
                    time_left += res.time();
        
        self.__queue[curr_res.id].append({curr_user: Resource(curr_res.id, time_left)})
    
    def dequeue(self,req_id, curr_user):
        curr_req = self.__queue[req_id]
        if len(curr_req):
            (first_item_key, _), = curr_req[0].items()
            if first_item_key.id == curr_user.id:
                self.__queue[req_id] = self.__queue[req_id][1:]
        
    def update(self):
        for (_, items) in self.__queue.items():
            for item in items:
                (_, item_value), = item.items()
                # if item_value.time() > 0:
                item_value.decrement()

    def last_queue(self, res_id = None):
        if len(self.__queue[res_id]) == 0:
            return None
        if res_id is not None:
            return self.__queue[res_id][-1]
    
    def in_queue(self, curr_user):
        for (_,user_list) in self.__queue.items():   
            for user_dict in user_list:
                (user_key, _), = user_dict.items()
                if user_key.id == curr_user.id:
                    return True
        return False
    
    def is_empty(self):
        for user in self.__queue.values():
            if len(user):
                return False
        return True
    
    def __repr__(self):
        return '%s' % self.__queue
    
class Simulation:
    def __init__(self, res_list, users):
        self.__queue = Queue(res_list)
        self.__process = {}
        self.__clock = 0
        self.__users = users
        self.initialize(users)
        
    def initialize(self, users):
        for user in users:
            if not user.is_complete():
                curr_user_req = user.curr_req()
                if not self.in_process(curr_user_req,user):                     
                    if self.is_next(curr_user_req.id, user):
                        self.delete(curr_user_req.id, user)
                        self.add_process(user, curr_user_req)
                elif not self.__queue.in_queue(user):
                    self.add_queue(curr_user_req, user)     
    
    def time(self):
        return self.__clock
    
    def time_up(self):
        self.__clock += 1

    def queue(self):
        return self.__queue.queue()
    
    def process(self):
        return self.__process

    def is_next(self, req_id, next_user):
        curr_queue = self.__queue.queue()[req_id]
        if len(curr_queue):
            (curr_user, _), = curr_queue[0].items()            
            return curr_user.id == next_user.id        
        return True

    def add_queue(self, curr_res, curr_user):
        self.__queue.enqueue(self.__process, curr_res, curr_user)
    
    def update_queue(self):
        self.__queue.update()
    
    def add_process(self, curr_user, req_id):
        self.__process[curr_user] = req_id
        
    def in_process(self, curr_req, curr_user):
        return any(1 if curr_req.id == req.id and curr_user.id != user.id else 0 for (user,req) in self.__process.items())
    
    def remove(self, curr_user):
        self.__process.pop(curr_user)
    
    def delete(self, req_id, curr_user):
        self.__queue.dequeue(req_id, curr_user)
    
    def in_queue(self,  user):
        self.__queue.in_queue(user)
        
    def status(self):
        for user in self.__users:
            print("U%d Requests:\n%s" % (user.id, user.req_list() if len(user.req_list()) > 0 else 'No Requests Left!'))

    def status(self):
        length = 30
        print("TIME ELAPSED: %ds\n" % self.time())        
        print("\n"+ length * "=" + " CURRENT PROCESSES " + length * "=") 
        for user in self.__users:
            print("User %d (U%d) Requests:\n%s\n" % (user.id, user.id, ' --- '.join(user.show_req()).ljust(10) if len(user.req_list()) > 0 else 'No Requests Left!'))
        
        print(length * "=" + " QUEUE/IN WAITING " + length * "=") 
        
        if self.__queue.is_empty():
            print("\nNo Users Waiting!\n")
            return
            
        for (res_id, user_list) in self.queue().items():
            if len(user_list) > 0:
                print("Resource %d (R%d):" % (res_id, res_id))
                for item in user_list:
                    (user, res), = item.items()
                    print("\tUser %d (Time Left: %ds)" % (user.id, res.time()))
                print()
        
def unique_list(n, in_list = None):  
    l = []  
    
    if in_list is None:
        count = 0
        while count < n:
            rnd_n = int(random() * 30) + 1
            if rnd_n not in l:
                l.append(rnd_n)
                count += 1
            
    else:      
        l = sample(in_list,n)

    return sorted(l)

def user_array(user_list, res):
    users = list(map(User,user_list))  
    
    for user in users:
        req_num = int(random() * len(res)) + 1
        req_list = list(map(lambda x: Resource(x,int(random() * 10) + 1),unique_list(req_num, res)))
        
        user.res_request(req_list);
       
    return users
                        
def main():
    resource_num = int(random() * 30) + 1
    user_num = int(random() * 30) + 1
    available_res = unique_list(resource_num)  # this one
    user_list = unique_list(user_num) # this one
    users = user_array(user_list, available_res)
    sim = Simulation(available_res, users)
    
    while len(sim.process()):
        # sleep(0.5)        
        system('cls')
        
        sim.status()
        input("Press Enter to continue")
        for (user, res) in list(sim.process().items()):
            if res.is_done():
                sim.remove(user)
                sim.initialize(users)
            else:                
                res.decrement()
        sim.time_up()    
        sim.update_queue()
         
    system('cls')
    sim.status()
    print("ALL PROCESSES DONE! ELAPSED TIME: %ds" % sim.time())    
    
    return

main()