from random import randint, sample

class Resource:
    def __init__(self, id, time):
        self.id = id
        self.__time = time
    
    def decrement(self):
        self.__time -= 1
    
    def is_done(self):
        return self.__time < 0
    
    def __repr__(self):
        return 'R%d, Time: (%d s)' % (self.id, self.__time)
    
class User:
    def __init__(self, id):
        self.id = id
        self.__res_list = []
    
    def is_complete(self):
        return False if self.__res_list else True
    
    def res_request(self, l):
        self.__res_list = l
    
    def curr_req(self):
        return self.__res_list[0]
    
    def dump_req(self):
        self.__res_list = self.__res_list[1:]

    def display(self):
        return 'U%d\n|-- Requests: ' % self.id + '{0}'.format(self.__res_list) if len(self.__res_list) > 0 else None

    def __repr__(self):
        return 'U%d' % self.id
    
class Simulation:
    def __init__(self, res_list):
        self.__queue = {res: [] for res in res_list}
        self.__process = {}
        self.__clock = 0
    
    def time(self):
        return self.__clock
    
    def time_up(self):
        self.__clock += 1

    def queue(self):
        return self.__queue
    
    def process(self):
        return self.__process
        # return {user:req.id for (user,req) in self.__process.items()}        

    def first_queue(self):
        return {res:(users[0] if len(users) else -1) for (res,users) in self.__queue.items()}

    def add_queue(self, res_id, curr_user):
        self.__queue[res_id] += [curr_user]
    
    def update_queue(self, res):
        self.__queue[res] =  self.__queue[res][1:]
    
    def add_process(self, curr_user, req_id):
        self.__process[curr_user] = req_id
        
    def in_process(self, curr_req):
        return any(1 if curr_req.id == req.id else 0 for (user,req) in self.__process.items())
    
    def remove(self, curr_user):
        self.__process.pop(curr_user)
    
    def delete(self, req_id, curr_user):
        curr_req = self.__queue[req_id]
        if len(curr_req):
            if curr_req[0].id == curr_user.id:
                print("AFTER CUT:",curr_req[1:])
                self.__queue[req_id] = curr_req[1:]
                print("UPDATED QUEUE OF R%d" % req_id,":",self.__queue[req_id])
        # if any(1 if curr_user.id == user.id else 0 for user in self.__queue[req_id]):
        #     print("NAA SA DIRI:",self.__queue[req_id])
        # else:
        #     print("WALA PA SA QUEUE")
    
    def in_queue(self, curr_user):
        for (req,user_list) in self.__queue.items():            
            if any(1 if curr_user.id == user.id else 0 for user in user_list):
                return True
        return False
        # return any(1 if curr_user.id == req.id else 0 for (user,req) in self.__queue.items())

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
        # while u_idx < self.__res_len and r_idx < self.__user_len:
        
def unique_list(n, in_list = None):  
    l = []  
    
    if in_list is None:
        count = 0
        # r_list = list(range(1,10))
        # l = sample(r_list, n)
        while count < n:
            rnd_n = randint(1,10)
            if rnd_n not in l:
                l.append(rnd_n)
                count += 1
            
    else:      
        l = sample(in_list,n)
        # for _ in range(n): 
        # while count < n:      
        #     idx = randint(0,len(res_list) - 1)        
        #     if res_list[idx] not in l:
        #         l.append(res_list[idx])
        #         count += 1

    return sorted(l)

def user_array(user_list, res):
    users = list(map(User,user_list))  
    # for user in users:
    #     req_num = randint(1, len(res))
    #     print("REQ NUM: ", req_num)
    #     req_list = list(map(lambda x: Resource(x,randint(1,5)),unique_list(req_num, res)))
        
    #     user.res_request(req_list);
        
    #     print('user: ', user)
    #     # print("REQUEST LIST: ", req_list)
    #     print()  
    users[0].res_request([Resource(5,5), Resource(8,10), Resource(30,15)])
    users[1].res_request([Resource(5,5), Resource(7,6), Resource(8,7)])
    users[2].res_request([Resource(5,8), Resource(30,5), Resource(25,4)])
    users[3].res_request([Resource(25,10)])
        
    return users
    
def initialize(sim, users):
    for user in users:
        print(user, "TYPE: ",type(user))
        if user.is_complete():
            print("U%d complete!" % user.id)
        else:
            curr_user_req = user.curr_req()
            # print("PROCESS VALUES: ",sim.process().values())
            # print("SIM VALUES: ",sim.process().values())
            # if curr_user_req.id not in sim.process().values(): # change to curr_user_req
            
            # if naay naggamit sa current resource
            if not sim.in_process(curr_user_req): 
                print("\n\nNEXT RESOURCE %d BY USER %d" % (curr_user_req.id,user.id))
                user.dump_req()
                sim.delete(curr_user_req.id, user)
                sim.add_process(user, curr_user_req)
            else:
                print("\n\nRESOURCE %d IS CURRENTLY TAKEN!" % curr_user_req.id)
                # print("CURR USER TO QUEUE: ",curr_user_req)   
                if not sim.in_queue(user):
                    print("IN PROCESS AND NOT IN QUEUE")
                    sim.add_queue(curr_user_req.id, user)
                else:
                    print("IN PROCESS AND IN QUEUE: %d" % user.id)
            print("DISPLAY: ",user.display())
                
    return sim
                        
def main():
    resource_num = randint(1, 10)
    # resource_num = randint(1, 30)
    user_num = 5
    # user_num = randint(1, 10) # this one
    # user_num = randint(1, 30)
    available_res = [5, 7, 8, 25, 30]
    # available_res = unique_list(resource_num)  # this one
    user_list = [5, 9, 11, 23]
    # user_list = unique_list(user_num) # this one
    # user_list = list(map(User,unique_list(user_num)))  
    users = user_array(user_list, available_res)
    print('available: ', available_res) 
    print('number of users: ', user_num)
    print('user: ', users)

    sim = Simulation(available_res)
    display = Display(available_res, user_list)
    display.header()
    print('\n===============================\n')    
    
    
    sim = initialize(sim, users)
    
    # while sim.time() < 5:
    while len(sim.process()):
        # input("\nPress enter\n")
        print("TIME ELAPSED: %ds" % sim.time())
        
        
        # for user in users:
        #     print(user, "TYPE: ",type(user))
        #     curr_user_req = user.curr_req()
        #     # print("PROCESS VALUES: ",sim.process().values())
        #     # print("SIM VALUES: ",sim.process().values())
        #     # if curr_user_req.id not in sim.process().values(): # change to curr_user_req
            
        #     # if naay naggamit sa current resource
        #     if not sim.in_process(curr_user_req): 
        #         sim.add_process(user.id, curr_user_req)
        #     else:
        #         # print("CURR USER TO QUEUE: ",curr_user_req)   
        #         if not sim.in_queue(user):
        #             sim.add_queue(curr_user_req.id, user)
        #     # print("CURR REQUEST: ", user.curr_req(), "ID: ", curr_user_req)
        #     # print("PROCESS: ", sim.process())
            
            
            
        print("QUEUE:\n", sim.queue())
        print("FIRST QUEUE:\n", sim.first_queue())
        print("PROCESSES: ", sim.process())
        
        print("IN LOOP PROCESS")
        for (user, res) in list(sim.process().items()):
            if res.is_done():
                print(res,"IS DONE!")
                print("\nSIM PROCESS:", sim.process())
                print()
                # user.dump_req()
                sim.remove(user)
                print("DISPLAY: ",user.display())
                sim = initialize(sim, users)
                print("UPDATED PROCESS: ", sim.process())
            # else:    
            print(user,": ", res, sep="")
            res.decrement()
                
        sim.time_up()    
        
    print("ALL PROCESSES DONE! ELAPSED TIME: %ds" % sim.time())    
    
    return



main()