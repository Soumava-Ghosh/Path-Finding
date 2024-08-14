import graph_DS,Priority_Queue

def dijkatra(graph,start):
    previous={v:None for v in graph.adjacency_list.keys()}
    visited={v:False for v in graph.adjacency_list.keys()}
    distances={v:float('inf') for v in graph.adjacency_list.keys()}
    distances[start]=0
    queue=Priority_Queue.PriorityQueue()
    queue.add_task(0,start)
    while queue:
       removed_distance,removed=queue.pop_task() 
       visited[removed]=True
       for edge in graph.adjacency_list[removed]:
           if visited[edge.vertex]:
               continue
           new_distance=removed_distance+edge.distance
           if new_distance<distances[edge.vertex]:
               distances[edge.vertex]=new_distance
               previous[edge.vertex]=removed
               queue.add_task(new_distance,edge.vertex)
    return
