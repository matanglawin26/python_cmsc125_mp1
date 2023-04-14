def is_next(self, req_id, next_user):
        curr_queue = self.__queue[req_id]
        if len(curr_queue):
            return curr_queue[0].id == next_user.id        
        return True