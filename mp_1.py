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
        return self.__time == 0
    
    def __repr__(self):
        return 'R%d, Time: (%d s)' % (self.id, self.__time) if not self.is_done() else 'R%d Complete!' % self.id
    
class User:
    def __init__(self, id):
        self.id = id
        self.__res_list = []
    
    # def is_complete(self):
    #     return False if self.__res_list else True
    
    def is_complete(self):
        return not self.curr_req()
    
    def req_list(self):
        return self.__res_list
    
    def res_request(self, l):
        self.__res_list = l
    
    def show_req(self):
        return [str(req) for req in self.__res_list]
    
    # def curr_req(self):
    #     return self.__res_list[0]
    
    def curr_req(self):
        for res in self.__res_list:
            if not res.is_done():
                return res
        return None
    
    # def dump_req(self):
        # self.__res_list = self.__res_list[1:]

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
            time_left += last_item_key.curr_req().time() + 1 
        else: # If no users are in queue
            for (user_id, res) in process.items():
                if curr_res.id == res.id:
                    time_left += res.time();
        
        self.__queue[curr_res.id].append({curr_user: Resource(curr_res.id, time_left)})
    
    def dequeue(self,req_id, curr_user):
        curr_req = self.__queue[req_id]
        if len(curr_req):
            (first_item_key, first_item_value), = curr_req[0].items()
            if first_item_key.id == curr_user.id:
                self.__queue[req_id] = self.__queue[req_id][1:]
        
    def update(self):
        for (res_id, items) in self.__queue.items():
            for item in items:
                (item_key, item_value), = item.items()
                if item_value.time() > 0:
                    item_value.decrement()

    def last_queue(self, res_id = None):
        if len(self.__queue[res_id]) == 0:
            return None
        if res_id is not None:
            return self.__queue[res_id][-1]
    
    def in_queue(self, curr_user):
        # print("CURRENT Q:",self.__queue)
        for (req,user_list) in self.__queue.items():   
            for user_dict in user_list:
                (user_key, user_value), = user_dict.items()
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
            (curr_user, curr_res), = curr_queue[0].items()            
            return curr_user.id == next_user.id        
        return True

    def add_queue(self, curr_res, curr_user):
        self.__queue.enqueue(self.__process, curr_res, curr_user)
        # timeLeft = 0
        # queuedItem = self.__queue[curr_res.id]
        
        # if len(queuedItem) == 0:
        #     for (user_id, res) in self.__process.items():
        #         if curr_res.id == res.id:
        #             timeLeft += res.time();
        # else:
        #     print("KEYS: ",queuedItem.keys())
        #     last_key = list(queuedItem.keys())[-1]
        #     print("LAST KEY: ",queuedItem[last_key], "TYPE:",type(last_key))
        #     timeLeft += self._getTime(last_key, curr_res.id)
        #     timeLeft += queuedItem[last_key]
        
        # self.__queue[curr_res.id][curr_user] = timeLeft
    
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
        return
        curr_req = self.__queue[req_id]
        if len(curr_req):
            first_key = next(iter(curr_req))
            if first_key.id == curr_user.id:
                self.__queue[req_id].pop(first_key)
                # self.__queue[req_id] = curr_req[1:]
    
    # def in_queue(self, curr_user):
    #     for (req,user_list) in self.__queue.items():         
    #         if any(1 if curr_user.id == user.id else 0 for (user, time) in user_list.items()):
    #             return True
    #     return False    
    def in_queue(self,  user):
        self.__queue.in_queue(user)
        
    def status(self):
        for user in self.__users:
            print("U%d Requests:\n%s" % (user.id, user.req_list() if len(user.req_list()) > 0 else 'No Requests Left!'))

    def status(self):
        print("TIME ELAPSED: %ds\n" % self.time())        
        print("\n"+30*"="+" CURRENT PROCESSES "+30*"=")
        for user in self.__users:
            print("User %d (U%d) Requests:\n%s\n" % (user.id, user.id, ' --- '.join(user.show_req()).ljust(10) if len(user.req_list()) > 0 else 'No Requests Left!'))
        
        print(30*"="+" QUEUE/IN WAITING "+30*"=")
        
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

class Display:
    def __init__(self, res_list, user_list):
        self.__res_list = res_list
        self.__user_list = user_list
        self.__res_len = len(res_list)
        self.__user_len = len(user_list)
    
    def header(self):
        u_idx = 0
        r_idx = 0
        
        print('%d Resources\t\t%d Users' % (self.__res_len, self.__user_len))
    
    def status(self, users):
        print("SUD STATUS")
        for user in users:
            print(user.display())
        return True
        
def unique_list(n, in_list = None):  
    l = []  
    
    if in_list is None:
        count = 0
        while count < n:
            rnd_n = int(random() * 30) + 1
            # rnd_n = randint(1,10)
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
        # req_num = randint(1, len(res))
        print("REQ NUM: ", req_num)
        req_list = list(map(lambda x: Resource(x,int(random() * 10) + 1),unique_list(req_num, res)))
        
        user.res_request(req_list);
        
        print('user: ', user)
        # print("REQUEST LIST: ", req_list)
        print()  
    
    # users[0].res_request([Resource(6,6)])
    # users[1].res_request([Resource(15,4)])
    # users[2].res_request([Resource(12,7)])
    # users[3].res_request([Resource(6,3), Resource(12,4), Resource(15,1)])
    # users[4].res_request([Resource(15,7)])
    # users[5].res_request([Resource(6,1), Resource(12,1), Resource(27,2)])
    # users[6].res_request([Resource(6,2)])
    # users[7].res_request([Resource(27,5)])
    # users[8].res_request([Resource(12,2), Resource(15,9)])
    # users[9].res_request([Resource(12,9)])
    
    # users[0].res_request([Resource(5,5), Resource(8,10), Resource(30,15)])
    # users[1].res_request([Resource(5,5), Resource(7,6), Resource(8,7)])
    # users[2].res_request([Resource(5,8), Resource(30,5), Resource(25,4)])
    # users[3].res_request([Resource(25,10)])
        
    return users
    
# def initialize(sim, users):
#     for user in users:
#         if not user.is_complete():
#             curr_user_req = user.curr_req()
#             if not sim.in_process(curr_user_req): 
#                 user.dump_req()
#                 sim.delete(curr_user_req.id, user)
#                 sim.add_process(user, curr_user_req)
#             else:
#                 sim.add_queue(curr_user_req.id, user)
                
#     return sim
                        
def main():
    # resource_num = randint(1, 10)
    resource_num = int(random() * 30) + 1
    # user_num = 5
    # user_num = randint(1, 10) # this one
    user_num = int(random() * 30) + 1
    # available_res = [5, 7, 8, 25, 30]
    # available_res = [6, 12, 15, 27]
    available_res = unique_list(resource_num)  # this one
    # user_list = [3, 4, 9, 14, 20, 21, 23, 25, 26, 27]
    # user_list = [5, 9, 11, 23]
    user_list = unique_list(user_num) # this one
    # user_list = list(map(User,unique_list(user_num)))  
    users = user_array(user_list, available_res)
    print('available: ', available_res) 
    print('number of users: ', user_num)
    print('user: ', users)
    sim = Simulation(available_res, users)
    display = Display(available_res, user_list)
    display.header()
    print('\n===============================\n')    
    # sim.queue()
    # sim = initialize(sim, users)
    
    # while sim.time() < 5:
    while len(sim.process()):
        # sleep(0.5)        
        system('cls')
        
        sim.status()
        sim.update_queue()
        # input("Press Enter to continue")
        for (user, res) in list(sim.process().items()):
            # print(user.display())
            if res.is_done():
                sim.remove(user)
                # sim = initialize(sim, users)
                # user.dump_req()
                sim.initialize(users)
            else:                    
                res.decrement()
            # sim.status()
            # print(user,": ", res, sep="")
        
        sim.time_up()    
         
    system('cls')
    sim.status()
    print("ALL PROCESSES DONE! ELAPSED TIME: %ds" % sim.time())    
    
    return



main()