from pprint import pprint
'''
2d Array to represent maze:
0 - Empty cell
1 - Wall
3 - Starting Point
4 - Ending Point
'''

lines = [line.rstrip('\n') for line in open('mazes/maze1.txt')]

grid = []
for line in lines:
    grid.append(line.split(','))



pprint(grid)
