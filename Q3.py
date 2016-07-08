import copy
import csv
import pprint
import random
import numpy as np
import itertools as it

ASPRIATION = False
RAND_START = False
ITERATIONS = 1000
RAND_TABU_LENGTH = False
SLICE_NEIGHBORS = False


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


def decrement_tabu(d):
    for i in d:
        if d[i] > 0:
            d[i] -= 1


# set up 2d arrays for flow and distance
flow = list(csv.reader(open("q3_csv/Flow.csv"), delimiter=','))
flow = [[int(string) for string in inner] for inner in flow]
flow = np.array(flow)
distance = list(csv.reader(open("q3_csv/Distance.csv"), delimiter=','))
distance = [[int(string) for string in inner] for inner in distance]
distance = np.array(distance)

# initial permutation
p = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

if RAND_START:
    random.shuffle(p)

# optimized P
p_opt = [18, 14, 10, 3, 9, 4, 2, 12, 11, 16, 19, 15, 20, 8, 13, 17, 5, 7, 1, 6]

# initial cost
cost = cost_function(flow, distance, p)
print "Cost:", cost, "Starting Point:", p

tabu_list = {}

prev_cost = cost
min_cost = cost
min_p = p

for t in xrange(ITERATIONS):
    decrement_tabu(tabu_list)
    d = dict()
    d2 = dict()

    combs = list(it.combinations(p, 2))

    if SLICE_NEIGHBORS:
        combs = random.sample(combs, len(combs) / 2)

    for i, elem in enumerate(combs):
        perm = swap_index(p, elem)
        cost = cost_function(flow, distance, perm)
        d[elem] = cost
        d2[elem] = cost

    minimum = min(d, key=d.get)

    while minimum in tabu_list and tabu_list[minimum] > 0:
        del d[minimum]
        minimum = min(d, key=d.get)

    if RAND_TABU_LENGTH:
        tabu_list[minimum] = random.randint(10, 20)
    else:
        tabu_list[minimum] = 10

    # Aspiration, take random if previous cost is greater or equal to curent
    if ASPRIATION:
        if d[minimum] >= prev_cost:
            minimum = random.choice(d2.keys())
        prev_cost = d2[minimum]

    p = swap_index(p, minimum)
    cost = cost_function(flow, distance, p)

    if min_cost > cost:
        min_cost = cost
        min_p = p

    print "Cost:", cost, "Permutation:", p, "Swap:", minimum, "T:", t + 1, "\tMin Cost:", min_cost

print "Cost:", min_cost, "Found:", min_p
# print cost_function(flow, distance, p_opt), p_opt
