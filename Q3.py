import copy
import csv
import json
import numpy as np
import itertools as it

# cost calculating cost function


def cost_function(f, d, p):
    temp1 = np.copy(f)
    for i, elem in enumerate(f):
        temp1[i, :] = f[p[i] - 1, :]

    temp2 = np.copy(temp1)
    for i, elem in enumerate(temp1):
        temp2[:, i] = temp1[:, p[i] - 1]

    return sum(np.diag(temp2.dot(d)))


def swap_index(p, s):
    temp = copy.deepcopy(p)
    i = s[0] - 1
    j = s[1] - 1
    temp[i], temp[j] = temp[j], temp[i]
    return temp


# set up 2d arrays for flow and distance
flow = list(csv.reader(open("q3_csv/Flow.csv"), delimiter=','))
flow = [[int(string) for string in inner] for inner in flow]
flow = np.array(flow)
distance = list(csv.reader(open("q3_csv/Distance.csv"), delimiter=','))
distance = [[int(string) for string in inner] for inner in distance]
distance = np.array(distance)

# initial permutation
p = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# initial cost
cost = cost_function(flow, distance, p)
print "Cost:", cost, "Permutation:", p

# iterations
T = 100
tabu_list = {}
for t in xrange(T):
    d = dict()
    combs = list(it.combinations(p, 2))
    for i, elem in enumerate(combs):
        perm = swap_index(p, elem)
        cost = cost_function(flow, distance, perm)
        d[elem] = cost

    minimum = min(d, key=d.get)
    while minimum in tabu_list:
        del d[minimum]
        minimum = min(d, key=d.get)
        
    tabu_list[minimum] = True

    p = swap_index(p, minimum)
    print "Cost:", cost_function(flow, distance, p), "Permutation:", p, "Swap:", minimum, "T:", t + 1
