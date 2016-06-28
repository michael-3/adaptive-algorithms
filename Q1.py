'''
2d Array to represent maze:
0 - Empty cell
1 - Wall
3 - Starting Point
4 - Ending Point
'''

from Queue import Queue
import heapq


class PriorityQueue:
    '''
    priority queue for a* search
    '''

    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def empty(self):
        return self._queue == []


def get_neighbors(arr, cur):
    '''
    Get Neighbors of cells
    '''
    cols = len(arr)
    rows = len(arr[0])
    r = cur[0]
    c = cur[1]
    neighbors = []

    # top
    if (r - 1) > -1:
        neighbors.append((r - 1, c))

    # right
    if (c + 1) < cols:
        neighbors.append((r, c + 1))

    # bottom
    if (r + 1) < rows:
        neighbors.append((r + 1, c))

    # left
    if (c - 1) > -1:
        neighbors.append((r, c - 1))

    return neighbors


def find(arr, el):
    '''
    Find Start and End cells
    '''
    for i, x in enumerate(arr):
        for j, y in enumerate(x):
            if y == el:
                return i, j
    return -1, -1


def bfs(grid, start):
    fringe = Queue()
    fringe.put(start)
    print "Starting at {}".format(start)
    visited = {}
    visited[start] = True

    while not fringe.empty():
        current = fringe.get()
        print "Visiting at {}".format(current)
        if grid[current[0]][current[1]] == '4':
            print "Found {}".format(current)
            break

        for n in get_neighbors(grid, current):
            if n not in visited and grid[n[0]][n[1]] != '1':
                fringe.put(n)
                visited[n] = True


def dfs(grid, start):
    fringe = list()
    fringe.append(start)
    print "Starting at {}".format(start)
    visited = {}
    visited[start] = True

    while fringe:
        current = fringe.pop()
        print "Visiting at {}".format(current)
        if grid[current[0]][current[1]] == '4':
            print "Found {}".format(current)
            break

        for n in get_neighbors(grid, current):
            if n not in visited and grid[n[0]][n[1]] != '1':
                fringe.append(n)
                visited[n] = True


def heuristic(current, next):
    '''
    Manhattan Distance Heuristic
    '''
    a = abs(int(current[0]) - int(next[0]))
    b = abs(int(current[1]) - int(next[1]))
    return a + b


def a_star(grid, start, end):
    fringe = PriorityQueue()
    fringe.push(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not fringe.empty():
        current = fringe.pop()
        print "Visiting at {}".format(current)

        if current == end:
            print "Found {}".format(current)
            break

        for n in get_neighbors(grid, current):
            new_cost = cost_so_far[current] + heuristic(current, n)
            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[n] = new_cost
                priority = new_cost + heuristic(end, n)
                fringe.push(n, priority)
                came_from[n] = current


files = ['maze_e1.txt', 'maze_e2.txt', 'maze_e3.txt']
# files = ['maze_e1.txt']

for f in files:
    lines = [line.rstrip('\n') for line in open('mazes/' + f)]

    grid = []
    for line in lines:
        grid.append(line.split(','))

    start = find(grid, '3')
    end = find(grid, '4')

    print "Starting BFS for {}".format(f)
    print "==================="
    bfs(grid, start)
    print "Starting DFS for {}".format(f)
    print "==================="
    dfs(grid, start)
    print "Starting A_* for {}".format(f)
    print "==================="
    a_star(grid, start, end)
