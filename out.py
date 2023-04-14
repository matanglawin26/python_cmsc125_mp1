import random

class User:
    def __init__(self, user_id, resource, time):
        self.user_id = user_id
        self.resource = resource
        self.time = time
        
class Resource:
    def __init__(self, resource_id):
        self.resource_id = resource_id
        self.user = None
        self.time_left = 0
        
class Queue:
    def __init__(self):
        self.queue = []
        
    def add_user(self, user):
        self.queue.append(user)
        self.queue.sort(key=lambda x: x.user_id)
        
    def remove_user(self, user):
        self.queue.remove(user)
        
    def get_next_user(self):
        if len(self.queue) > 0:
            return self.queue[0]
        else:
            return None
        
class Simulation:
    def __init__(self, num_resources, num_users):
        self.resources = [Resource(i+1) for i in range(num_resources)]
        self.users = []
        self.queue = Queue()
        self.current_time = 0
        
        for i in range(num_users):
            resource = random.choice(self.resources)
            time = random.randint(1, 30)
            user = User(i+1, resource, time)
            self.users.append(user)
            
    def run(self):
        while True:
            # Check if any users have finished using a resource
            for resource in self.resources:
                if resource.user is not None and resource.time_left == 0:
                    resource.user.resource = None
                    resource.user = None
            
            # Check if any resources are available
            available_resources = [resource for resource in self.resources if resource.user is None]
            
            # Assign resources to waiting users
            for resource in available_resources:
                next_user = self.queue.get_next_user()
                if next_user is not None:
                    self.queue.remove_user(next_user)
                    resource.user = next_user
                    resource.time_left = next_user.time
            
            # Update time left for users using resources
            for resource in self.resources:
                if resource.user is not None:
                    resource.time_left -= 1
            
            # Add any new users that arrive at this time
            for user in self.users:
                if user.time == self.current_time:
                    if user.resource.user is None:
                        user.resource.user = user
                        user.resource.time_left = user.time
                    else:
                        self.queue.add_user(user)
            
            # Print status of resources and waiting users
            print(f"Time: {self.current_time}")
            for resource in self.resources:
                if resource.user is None:
                    print(f"Resource {resource.resource_id} is free.")
                else:
                    print(f"Resource {resource.resource_id} is being used by User {resource.user.user_id} for {resource.time_left} more seconds.")
            if len(self.queue.queue) > 0:
                print(f"Users waiting: {[user.user_id for user in self.queue.queue]}")
            
            # Check if all users have finished
            if all([resource.user is None for resource in self.resources]) and len(self.queue.queue) == 0:
                break
            
            # Increment current time
            self.current_time += 1

# Example usage
simulation = Simulation(num_resources=30, num_users=30)
simulation.run()
