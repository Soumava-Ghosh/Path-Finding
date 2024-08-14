'''

References
https://gamedev.stackexchange.com/questions/197165/java-simple-2d-grid-pathfinding
https://svn.sable.mcgill.ca/sable/courses/COMP763/oldpapers/yap-02-grid-based.pdf

'''
import pygame
import math
import heapq

class App:
    def __init__(self) -> None:
        self.HEIGHT,self.WIDTH=1200,600
        self.FPS=200
        self.CLOCK=pygame.time.Clock()
        self.WINDOW=pygame.display.set_mode((self.HEIGHT,self.WIDTH))
        self.x,self.y=None,None
        self.next=[]
        pass

    def run(self):
        grid=Grid()
        cols,rows=grid.getRowColumn()
        board=grid.make2dArray(cols,rows)
        mouse=mousepressed()
        dragging=False
        

        while True:  
            self.WINDOW.fill((211,211,211))
            pygame.display.set_caption(f"Path Finding {self.CLOCK.get_fps()}")
            

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit()
                elif event.type==pygame.KEYDOWN:
                    #Clears screen
                    if event.key==pygame.K_BACKSPACE:
                        board=grid.clearboard(board)
                    #Line drawing algorithm
                    if event.key==pygame.K_RETURN:
                        print(grid.distance(x1,y1,x2,y2),'Units')
                        # print(grid.giveCellsWhichAreinPath(x1,y1,x2,y2))
                        points=grid.giveCellsWhichAreinPath(x1,y1,x2,y2)
                        board=grid.colorPotentialPath(points,board)
                    #Djikster Algorithm 
                    if event.key==pygame.K_d:
                        start=(x1,y1)
                        goal=(x2,y2)
                        path=dijkstra(board,start,goal)
                        board=grid.colorPotentialPath(path,board)

                elif event.type==pygame.MOUSEBUTTONDOWN: #Mouse interactions Changes state of cells
                    if event.button==1:
                        self.x,self.y=mouse.select(event.pos)
                        board[self.x][self.y]=1
                        x1,y1=self.x,self.y
                    if event.button==3:
                        self.x,self.y=mouse.select(event.pos)
                        board[self.x][self.y]=2
                        x2,y2=self.x,self.y
                    if event.button==2:
                        dragging=True
                        self.x,self.y=mouse.select(event.pos)
                        board[self.x][self.y]=4
                elif event.type==pygame.MOUSEBUTTONUP:
                    if event.button==2:
                        dragging=False
                elif event.type==pygame.MOUSEMOTION:
                        if dragging:
                            self.x,self.y=mouse.select(event.pos)
                            board[self.x][self.y]=4


            grid.draw(board)
            pygame.display.flip()
            self.CLOCK.tick(self.FPS)	



class Grid(App):

    def __init__(self) -> None:
        super().__init__()
        self.resolution=20
        self.color='White'
        self.cols=int(self.HEIGHT/self.resolution)
        self.rows=int(self.WIDTH/self.resolution)

    def getRowColumn(self):
        return (self.cols,self.rows)
    
    #Colors the path
    def colorPotentialPath(self,pathpoints,board):
        if pathpoints:
            for i in pathpoints:
                x,y=i
                board[x][y]=3
        else:
            print("No Path")

        return board
    #Straightline distance from start to goal
    def distance(self,x1,y1,x2,y2):
        return math.sqrt(((x2-x1)*(x2-x1))+(y2-y1)*(y2-y1))
    #draws the grids based on their state 1.Starting 2.Goal 3.Path 4.Obstacle
    def draw(self,grid):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                x=i*self.resolution
                y=j*self.resolution
                # if grid[i][j]==1:
                match grid[i][j]:
                    case 1:
                        pygame.draw.rect(self.WINDOW,('Green'),pygame.Rect(x,y,self.resolution,self.resolution))   
                # if grid[i][j]==2:
                    case 2:
                        pygame.draw.rect(self.WINDOW,('Red'),pygame.Rect(x,y,self.resolution,self.resolution))
                    case 3:
                        pygame.draw.rect(self.WINDOW,('Yellow'),pygame.Rect(x,y,self.resolution,self.resolution))
                    case 4:
                        pygame.draw.rect(self.WINDOW,('Black'),pygame.Rect(x,y,self.resolution,self.resolution))

                pygame.draw.rect(self.WINDOW,('Black'),pygame.Rect(x,y,self.resolution,self.resolution),1)
    #Makes a 2d array
    def make2dArray(self,cols,rows):
        arr=[0]*cols
        for i in range(len(arr)):
            arr[i]=[0]*rows
        return arr
    #Sets all values to 0
    def clearboard(self,grid):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                grid[i][j]=0
        return grid
    
    def giveCellsWhichAreinPath(self,x0,y0,x1,y1):
        """
        Bresenham's Line Drawing Algorithm to find the points of a line between two points.
        """
        '''I understand nothing of this sh!t'''
        points = []

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            points.append((x0, y0))
            
            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * err

            if e2 > -dy:
                err -= dy
                x0 += sx

            if e2 < dx:
                err += dx
                y0 += sy
        points=points[1:-1]
        return points
    
#Djikster Algorithm implementation
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def enqueue(self, priority, element):
        heapq.heappush(self.elements, (priority, element))

    def dequeue(self):
        return heapq.heappop(self.elements)[1]

    def is_empty(self):
        return len(self.elements) == 0

# def dijkstra(grid, start, goal):
#     rows = len(grid)
#     cols = len(grid[0])
#     directions = [
#         (-1, 0), (1, 0), (0, -1), (0, 1),  # N, S, W, E
#         (-1, -1), (-1, 1), (1, -1), (1, 1)  # NW, NE, SW, SE
#     ]

#     distance = [[float('inf')] * cols for _ in range(rows)]
#     previous = [[None] * cols for _ in range(rows)]
#     pq = PriorityQueue()

#     distance[start[0]][start[1]] = 0
#     pq.enqueue(0, start)

#     while not pq.is_empty():
#         current = pq.dequeue()

#         if current == goal:
#             return reconstruct_path(previous, start, goal)

#         for dx, dy in directions:
#             neighbor = (current[0] + dx, current[1] + dy)
#             if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] != 4:
#                 new_dist = distance[current[0]][current[1]] + 1
#                 if new_dist < distance[neighbor[0]][neighbor[1]]:
#                     distance[neighbor[0]][neighbor[1]] = new_dist
#                     previous[neighbor[0]][neighbor[1]] = current
#                     pq.enqueue(new_dist, neighbor)

#     return None  # No path found


def dijkstra(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1)  # N, S, W, E
    ]

    distance = [[float('inf')] * cols for _ in range(rows)]
    previous = [[None] * cols for _ in range(rows)]
    pq = PriorityQueue()

    distance[start[0]][start[1]] = 0
    pq.enqueue(0, start)

    while not pq.is_empty():
        current = pq.dequeue()

        if current == goal:
            return reconstruct_path(previous, start, goal)

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] != 4:
                new_dist = distance[current[0]][current[1]] + 1
                if new_dist < distance[neighbor[0]][neighbor[1]]:
                    distance[neighbor[0]][neighbor[1]] = new_dist
                    previous[neighbor[0]][neighbor[1]] = current
                    pq.enqueue(new_dist, neighbor)

    return None  # No path found
def reconstruct_path(previous, start, goal):
    path = []
    current = goal
    while current:
        path.append(current)
        current = previous[current[0]][current[1]]
    path.reverse()
    path=path[1:-1]
    return path
       

#Returns the col and row number from screen coords 
class mousepressed(Grid):
    def __init__(self) -> None:
        super().__init__()
    
    def select(self,pos):
        x,y=pos[0]//self.resolution,pos[1]//self.resolution
        return (x,y)



if __name__=="__main__":
    app=App()
    app.run()