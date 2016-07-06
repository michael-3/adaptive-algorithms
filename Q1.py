'''
2d Array to represent maze:
0 - Empty cell
1 - Wall
3 - Starting Point
4 - Ending Point
'''

from Queue import Queue, PriorityQueue
import copy


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
    if (r - 1) > -1 and arr[r - 1][c] != '1':
        neighbors.append((r - 1, c))

    # right
    if (c + 1) < cols and arr[r][c + 1] != '1':
        neighbors.append((r, c + 1))

    # bottom
    if (r + 1) < rows and arr[r + 1][c] != '1':
        neighbors.append((r + 1, c))

    # left
    if (c - 1) > -1 and arr[r][c - 1] != '1':
        neighbors.append((r, c - 1))

    return neighbors


def get_path(d, start, end):
    s = str(start)
    e = str(end)
    path = list()
    val = d[e]
    path.append(end)
    coor = val.strip('()').split(',')
    path.append((int(coor[0]), int(coor[1])))
    while val != s:
        val = d[val]
        coor = val.strip('()').split(',')
        path.append((int(coor[0]), int(coor[1])))
    return path


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
    path = {}

    while not fringe.empty():
        current = fringe.get()

        # print "Visiting at {}".format(current)

        if grid[current[0]][current[1]] == '4':
            print "Found {}".format(current)
            return get_path(path, start, current)
            break

        for n in get_neighbors(grid, current):
            if n not in visited and grid[n[0]][n[1]] != '1':
                path[str(n)] = str(current)
                fringe.put(n)
                visited[n] = True


def dfs(grid, start):
    fringe = list()
    fringe.append(start)
    print "Starting at {}".format(start)
    visited = {}
    visited[start] = True
    path = {}

    while fringe:
        current = fringe.pop()

        # print "Visiting at {}".format(current)

        if grid[current[0]][current[1]] == '4':
            print "Found {}".format(current)
            return get_path(path, start, current)
            break

        for n in get_neighbors(grid, current):
            if n not in visited and grid[n[0]][n[1]] != '1':
                path[str(n)] = str(current)
                fringe.append(n)
                visited[n] = True


class a_cell:

    def __init__(self, val):
        self.val = val
        self.h = 0
        self.g = 0
        self.parent = None


def heuristic(current, next):
    '''
    Manhattan Distance Heuristic
    '''
    a = abs(int(current[0]) - int(next[0]))
    b = abs(int(current[1]) - int(next[1]))
    return a + b


def in_queue(item, pq):
    for i in pq.queue:
        if i[1].val == item.val:
            return True
    return False


def a_star(grid, start, end):
    print "Starting at {}".format(start)

    start = a_cell(start)
    end = a_cell(end)

    # Priority to sort queue on heuristic values
    openset = PriorityQueue()
    closedset = set()
    openset.put((start.h + start.g, start))

    while openset:
        # Find the item in the open set with the lowest G + H score
        current = openset.get_nowait()[1]

        # print "Visiting at {}".format(current.val)

        if current.val == end.val:
            print "Found {}".format(current.val)
            path = []
            while current.parent:
                path.append(current.val)
                current = current.parent
            path.append(current.val)
            return path
            break

        # Add it to the closed set
        closedset.add(current)

        for neighbor in get_neighbors(grid, current.val):

            cell = a_cell(neighbor)

            # If it is already in the closed set, skip it
            if cell in closedset:
                continue

            # Otherwise if it is already in the open set
            if in_queue(cell, openset):
                # Check if we beat the G score
                new_g = current.g + 1
                if cell.g > new_g:
                    # If so, update the cell to have a new parent
                    cell.g = new_g
                    cell.parent = current
            else:
                # Not in open set, calculate the G and H score for cell
                cell.g = current.g + 1
                cell.h = heuristic(cell.val, end.val)

                # Set the parent to our current item
                cell.parent = current

                # Add it to the set
                openset.put((cell.h + cell.g, cell))


def print_grid(grid, path):
    g = copy.deepcopy(grid)
    for p in path:
        g[p[0]][p[1]] = ' '
    g[path[0][0]][path[0][1]] = 'x'
    g[path[len(path) - 1][0]][path[len(path) - 1][1]] = 'x'
    return g

files = ['maze_e1.txt', 'maze_e2.txt', 'maze_e3.txt']

for f in files:
    lines = [line.rstrip('\n') for line in open('mazes/' + f)]

    grid = []
    for line in lines:
        grid.append(line.split(','))

    start = find(grid, '3')
    end = find(grid, '4')

    name = 'mazes/output_bfs_' + f
    out = open(name, 'w+')
    print "\nStarting BFS for {}".format(f)
    print "==================="
    path = bfs(grid, start)
    print >>out, "Path = {}\n".format(path)
    for row in print_grid(grid, path):
        print >>out, row

    name = 'mazes/output_dfs_' + f
    out = open(name, 'w+')
    print "\nStarting DFS for {}".format(f)
    print "==================="
    path = dfs(grid, start)
    print >>out, "Path = {}\n".format(path)
    for row in print_grid(grid, path):
        print >>out, row

    name = 'mazes/output_astar_' + f
    out = open(name, 'w+')
    print "\nStarting A_* for {}".format(f)
    print "==================="
    path = a_star(grid, start, end)
    print >>out, "Path = {}\n".format(path)
    for row in print_grid(grid, path):
        print >>out, row
