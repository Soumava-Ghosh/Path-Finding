import itertools,heapq
class PriorityQueue:
    def __init__(self) -> None:
        self.pq=[]                          # list of entries arranged in a heap
        self.enter_finder={}                # mapping of tasks to entries
        self.counter=itertools.count()      # unique sequence count
    
    def __len__(self):
        return len(self.pq)
    
    def add_task(self,priority,task):
        '''Add a new task or update the priority of an existing task'''
        if task in self.enter_finder:
            self.update_priority(priority,task)
            return self
        count=next(self.counter)
        entry=[priority,count,task]
        self.enter_finder[task]=entry
        heapq.heappush(self.pq,entry)

    def update_priority(self,priority,task):
        '''Update the priority of a task. Raise keyError is not found'''
        entry=self.enter_finder[task]
        count=next(self.counter)
        entry[0],entry[1]=priority,count

    def pop_task(self):
        ''' Remove and return the lowest priority task. Raise KeyError if empty'''
        while self.pq:
            priority,count,task=heapq.heappop(self.pq)
            del self.enter_finder[task]
            return priority,task
        raise KeyError('pop from an empty priority queue')