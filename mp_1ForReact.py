from random import randint, sample

class Resource:
    def __init__(self, id, time):
        self.id = id
        self.__time = time
    
    def decrement(self):
        self.__time -= 1
    
    def is_done(self):
        return self.__time == 0
    
    def __repr__(self):
        return 'R%d, Time: (%d s)' % (self.id, self.__time)
    
class User:
    def __init__(self, id):
        self.id = id
        self.__res_list = []
    
    def is_complete(self):
        return False if self.__res_list else True
    
    def req_list(self):
        return self.__res_list
    
    def res_request(self, l):
        self.__res_list = l
    
    def curr_req(self):
        return self.__res_list[0]
    
    def dump_req(self):
        self.__res_list = self.__res_list[1:]

    def display(self):
        return 'U%d\n|-- Requests: ' % self.id + '{0}'.format(self.__res_list) if len(self.__res_list) > 0 else ''

    def __repr__(self):
        return 'U%d' % self.id
    
class Simulation:
    def __init__(self, res_list, users):
        self.__queue = {res: [] for res in res_list}
        self.__process = {}
        self.__clock = 0
        self.__users = users
        self.initialize(users)
        
    def initialize(self, users):
        for user in users:
            if not user.is_complete():
                curr_user_req = user.curr_req()
                if not self.in_process(curr_user_req,user): 
                    self.delete(curr_user_req.id, user)
                    self.add_process(user, curr_user_req)
                elif not self.in_queue(user):
                    self.add_queue(curr_user_req.id, user)     
    
    def time(self):
        return self.__clock
    
    def time_up(self):
        self.__clock += 1

    def queue(self):
        return self.__queue
    
    def process(self):
        return self.__process

    def first_queue(self):
        return {res:(users[0] if len(users) else -1) for (res,users) in self.__queue.items()}

    def add_queue(self, res_id, curr_user):
        self.__queue[res_id] += [curr_user]
    
    def update_queue(self, res):
        self.__queue[res] =  self.__queue[res][1:]
    
    def add_process(self, curr_user, req_id):
        self.__process[curr_user] = req_id
        
    def in_process(self, curr_req, curr_user):
        return any(1 if curr_req.id == req.id and curr_user.id != user.id else 0 for (user,req) in self.__process.items())
    
    def remove(self, curr_user):
        self.__process.pop(curr_user)
    
    def delete(self, req_id, curr_user):
        curr_req = self.__queue[req_id]
        
        if len(curr_req):
            if curr_req[0].id == curr_user.id:
                self.__queue[req_id] = curr_req[1:]
    
    def in_queue(self, curr_user):
        for (req,user_list) in self.__queue.items():            
            if any(1 if curr_user.id == user.id else 0 for user in user_list):
                return True
        return False    
    
    def status(self):
        for user in self.__users:
            print("U%d Requests:\n%s" % (user.id, user.req_list() if len(user.req_list()) > 0 else 'No Requests Left!'))

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
            rnd_n = randint(1,10)
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
    sim = Simulation(available_res, users)
    display = Display(available_res, user_list)
    display.header()
    print('\n===============================\n')    
    
    
    # sim = initialize(sim, users)
    
    # while sim.time() < 5:
    while len(sim.process()):
        print("TIME ELAPSED: %ds" % sim.time())
        print("\nQUEUE:", sim.queue())
        print("PROCESSES: ", sim.process())
        print()
        input("Press Enter to continue")
        print("\n\nSTATUS: ")
        sim.status()
        for (user, res) in list(sim.process().items()):
            # print(user.display())
            if res.is_done():
                sim.remove(user)
                # sim = initialize(sim, users)
                user.dump_req()
                sim.initialize(users)
            # else:    
            # sim.status()
            # print(user,": ", res, sep="")
            res.decrement()
        
        sim.time_up()    
        
    sim.status()
    print("ALL PROCESSES DONE! ELAPSED TIME: %ds" % sim.time())    
    
    return



main()