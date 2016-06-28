from Queue import Queue

'''
2d Array to represent maze:
0 - Empty cell
1 - Wall
3 - Starting Point
4 - Ending Point
'''


def get_neighbors(arr, cur):
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


files = ['maze_e1.txt', 'maze_e2.txt', 'maze_e3.txt']

for f in files:
    lines = [line.rstrip('\n') for line in open('mazes/' + f)]

    grid = []
    for line in lines:
        grid.append(line.split(','))
    start = find(grid, '3')
    print "Starting BFS for {}".format(f)
    print "==================="
    bfs(grid, start)
    print "Starting DFS for {}".format(f)
    print "==================="
    dfs(grid, start)


