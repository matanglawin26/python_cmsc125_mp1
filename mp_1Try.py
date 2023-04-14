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
        return self.__time <= 0
    
    def __repr__(self):
        return 'R%d, Time: (%d s)' % (self.id, self.__time)
    
    # def __repr__(self):
    #     return 'R%d, Time: (%d s)' % (self.id, self.__time) if not self.is_done() else 'R%d Complete!' % self.id
    
    def __str__(self):
        return 'R%d, Time: (%d s)' % (self.id, self.__time) if not self.is_done() else 'R%d Complete!' % self.id
    
class User:
    def __init__(self, id):
        self.id = id
        self.res_list = []
    
    def is_complete(self):
        return not self.curr_req()
    
    def req_list(self):
        return self.res_list
    
    def res_request(self, l):
        self.res_list = l
    
    def curr_req(self):
        for res in self.res_list:
            if not res.is_done():
                return res
        return None
    
    def dump_req(self):
        self.res_list.pop(0)

    def show_req(self):
        return [str(req) for req in self.res_list]

    def get_req(self, req_id):
        for res in self.res_list:
            if res.id == req_id:
                return res
        return None        

    def display(self):
        if self.res_list:
            return f"U{self.id}\n|-- Requests: {self.res_list}"
        else:
            return ""

    def __repr__(self):
        return f"U{self.id}"

class Queue:
    def __init__(self, res_list):
        self.__queue = {res: [] for res in res_list}
    
    def queue(self):
        return self.__queue
    
    def in_queue(self, curr_user):
        for res_id, users in self.__queue.items():
            for user_dict in users:
                if curr_user.id == list(user_dict.keys())[0].id:
                    return True
        return False

    def enqueue(self, sim, curr_res, curr_user):
        time_left = 0
        if len(self.__queue[curr_res.id]) > 0:
            last_user_dict = self.__queue[curr_res.id][-1]
            last_user = list(last_user_dict.keys())[0]
            time_left += last_user_dict[last_user].time()
        elif curr_res.id in sim.process():
            last_user = sim.process()[curr_res.id]
            time_left += last_user.time()

        self.__queue[curr_res.id].append({curr_user: Resource(curr_res.id, time_left)})
    
    def dequeue(self, req_id, curr_user):
        for user_dict in self.__queue[req_id]:
            if curr_user.id == list(user_dict.keys())[0].id:
                self.__queue[req_id].remove(user_dict)
                break
    # def enqueue(self, sim, curr_res, curr_user):
    #     time_left = 0
    #     last_item = self.last_queue(curr_res.id)
    #     if last_item:
    #         last_item_key, last_item_value = next(iter(last_item.items()))
    #         print("SUD IF LAST!", last_item_key, "VALUE:",last_item_value)
    #         time_left += last_item_value.time()
    #         time_left += last_item_key.get_req(curr_res.id).time()
    #     else: # If no users are in queue
    #         res = sim.get_task(curr_res)
    #         if(res):
    #             print("SUD ELSE:", res)
    #             time_left += res.time()
    #         # for (user_id, res) in process.items():
    #         #     if curr_res.id == res.id:
    #         #         time_left += res.time();
        
    #         print("\nPROCESS:", sim.process())
    #         # print("QUEUE:", self.__queue)
    #         print("USER ID:", curr_user, "RES:", curr_res, "TIME LEFT:",time_left)
    #         input("ZERO")
            
    #     self.__queue[curr_res.id].append({curr_user: Resource(curr_res.id, time_left)})
    
    # def dequeue(self,req_id, curr_user):
    #     curr_req = self.__queue[req_id]
    #     print("self.__queue[27]:",self.__queue[12])
    #     if len(self.__queue[12]):
    #         print("CURR QUEUE:",self.__queue)
    #         print("USER 27:", self.__queue[12])
    #         input("USER 27!!!")
    #     if len(curr_req):
    #         (first_item_key, first_item_value), = curr_req[0].items()
    #         if first_item_key.id == curr_user.id:
    #             self.__queue[req_id] = self.__queue[req_id][1:]
        
    def update(self):
        for (res_id, items) in self.__queue.items():
            for item in items:
                (item_key, item_value), = item.items()
                item_value.decrement()

    def last_queue(self, res_id = None):
        if len(self.__queue[res_id]) == 0:
            return None
        if res_id is not None:
            return self.__queue[res_id][-1]
    
    # def in_queue(self, curr_user):
    #     for (req,user_list) in self.__queue.items():   
    #         for user_dict in user_list:
    #             (user_key, user_value), = user_dict.items()
    #             if user_key.id == curr_user.id:
    #                 return True
    #     return False
    
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
            print("DATA:", user.display())
            if not user.is_complete():
                curr_user_req = user.curr_req()                
                if not self.in_process(curr_user_req,user): 
                    # if self.__queue.in_queue(user):
                    self.delete(curr_user_req.id, user)
                    self.add_process(user, curr_user_req)
                elif not self.__queue.in_queue(user):
                    self.add_queue(curr_user_req, user)     
        print('\n\n')
    def time(self):
        return self.__clock
    
    def time_up(self):
        self.__clock += 1

    def queue(self):
        return self.__queue.queue()
    
    def process(self):
        return self.__process

    def get_task(self, curr_res):
        for (user_id, res) in self.__process.items():
            if curr_res.id == res.id:
                return res
        return None
    
    def add_queue(self, curr_res, curr_user):
        self.__queue.enqueue(self, curr_res, curr_user)
    
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
        print("TIME ELAPSED: %ds\n" % self.time())        
        print("\n"+30*"="+" CURRENT PROCESSES "+30*"=")
        for user in self.__users:
            print("User %d (U%d) Requests:\n%s\n" % (user.id, user.id, ' --- '.join(user.show_req()).ljust(10) if len(user.req_list()) > 0 else 'No Requests Left!'))
        
        print(30*"="+" QUEUE/IN WAITING "+30*"=")
        for (res_id, user_list) in self.queue().items():
            if len(user_list) > 0:
                print("Resource %d (R%d):" % (res_id, res_id))
                for item in user_list:
                    (user, res), = item.items()
                    print("\tUser %d (Time Left: %ds)" % (user.id, res.time()))
                print()
            else:
                print("\tNo Users Waiting!\n")

    def user_reqs(self):
        for user in self.__users:
            print("User %d (U%d) Requests:" % (user.id, user.id,))
            for res in user.req_list():
                print("\t%s" % res)
            print()

    def _getTime(self,user, res_id):
        req_list = user.req_list();
        for req in req_list:
            if req.id == res_id:
                return req.time()
        return 0;

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
            if rnd_n not in l:
                l.append(rnd_n)
                count += 1
            
    else:      
        l = sample(in_list,n)

    return sorted(l)

def user_array(user_list, res):
    users = list(map(User,user_list))  
    
    # for user in users:
    #     req_num = randint(1, len(res))
    #     req_list = list(map(lambda x: Resource(x,int(random() * 10) + 1),unique_list(req_num, res)))
        
    #     user.res_request(req_list)
        # print("REQUEST LIST: ", req_list)
    print("USERS:", users)
    users[0].res_request([Resource(6,6)])
    users[1].res_request([Resource(15,4)])
    users[2].res_request([Resource(12,7)])
    users[3].res_request([Resource(6,3), Resource(12,4), Resource(15,1)])
    users[4].res_request([Resource(15,7)])
    users[5].res_request([Resource(6,1), Resource(12,1), Resource(27,2)])
    users[6].res_request([Resource(6,2)])
    users[7].res_request([Resource(27,5)])
    users[8].res_request([Resource(12,2), Resource(15,9)])
    users[9].res_request([Resource(12,9)])
    
    # users[0].res_request([Resource(5,5), Resource(8,10), Resource(30,15)])
    # users[1].res_request([Resource(5,5), Resource(7,6), Resource(8,7)])
    # users[2].res_request([Resource(5,8), Resource(30,5), Resource(25,4)])
    # users[3].res_request([Resource(25,10)])
        
    return users
                        
def main():
    resource_num = int(random() * 10) + 1
    resource_num = 5 # del this one
    # resource_num = randint(1, 30)
    # user_num = 5
    user_num = int(random() * 10) + 1 # this one
    user_num = 10 # del this one
    # user_num = randint(1, 30)
    available_res = [6, 12, 15, 27]
    # available_res = unique_list(resource_num)  # this one
    user_list = [3, 4, 9, 14, 20, 21, 23, 25, 26, 27]
    # user_list = unique_list(user_num) # this one
    # user_list = list(map(User,unique_list(user_num)))  
    users = user_array(user_list, available_res)
    # print('available: ', available_res) 
    # print('number of users: ', user_num)
    # print('user: ', users)
    sim = Simulation(available_res, users)
    # display = Display(available_res, user_list)
    # display.header()
    # print('\n===============================\n')    
    sim.queue()
    # sim = initialize(sim, users)
    print(30*"="+" INITIAL DATA (USER REQUESTS) "+30*"=")
    sim.user_reqs()
    input("\nPress enter to start\n")
    # while sim.time() < 5:
    while len(sim.process()):
        # sleep(1)
        # system('cls')
        # print("PROCESSES: ", sim.process())
        # print()
        # input("Press Enter to continue")
        sim.status()
        input("PRESS TO CONTINUE")
        # print("\nQUEUE:", sim.queue())
        for (user, res) in list(sim.process().items()):
            # print(user.display())
            res.decrement()
            if res.is_done():
                sim.remove(user)
                # sim = initialize(sim, users)
                # user.dump_req()
                sim.initialize(users)
            # else:    
            # sim.status()
            # print(user,": ", res, sep="")
        
        sim.update_queue()
        sim.time_up()    
        
    sim.status()
    print("\nALL PROCESSES DONE!")
    print("\nTOTAL ELAPSED TIME: %ds" % sim.time())    
    
    return



main()