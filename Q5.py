'''
Annealing CVRP()

'''
import math
import random
import os
import copy
# Parser
# return hashmap of capacity for each node, hashmap of
# coordinates for each node


def parser(vrf):
    name = os.path.basename(vrf).split('-')
    nodes = int(''.join(c for c in name[1] if c.isdigit()))
    vehicles = int(''.join(c for c in name[2] if c.isdigit()))
    coordinates = {}
    customers = {}
    with open(vrf) as f:
        for i, line in enumerate(f):
            if i == 1:
                comment = line.split()
                optimal = ''.join(c for c in comment[-1] if c.isdigit())
            if i == 5:
                capacity = int(''.join(c for c in line if c.isdigit()))
            if i >= 7 and i < 7 + nodes:
                a = line.split()
                coordinates[int(a[0])] = int(a[1]), int(a[2])
            if i > 7 + nodes and i <= 7 + 2 * nodes:
                a = line.split()
                customers[int(a[0])] = int(a[1])

    return nodes, vehicles, capacity, coordinates, customers, optimal

# customers - hashmap of customers {customer: demand}
# return: hashmap of routes {route #: route}


def initialSolution(customers, capacity):
    solution = {}
    visited = [1]
    while len(visited) != len(customers):
        c = capacity
        route = [1]
        for customer in customers.keys():
            if customers[customer] <= c and customer not in visited:
                route.append(customer)
                visited.append(customer)
                c -= customers[customer]
        route.append(1)
        solution[len(solution)] = route
    return solution


def annealingCVRP(customers, capacity, coordinates, maxT):
    s = initialSolution(customers, capacity)
    print "Intial solution: ", s
    a = 0.95  # temp reduction multiplier
    b = 1.05  # iteration multiplier
    Mo = 5  # time to next param update
    T = 5000.
    best = s
    current_s = s
    current_cost = cost(s, coordinates)
    best_cost = current_cost
    print "Greedy cost: ", current_cost
    time = 0
    while time < maxT and T >= 0.001:
        M = Mo
        while (M >= 0):
            new_s = neighbor(current_s, capacity, customers)
            new_cost = cost(new_s, coordinates)
            delta_cost = new_cost - current_cost
            if delta_cost < 0:
                current_s = new_s
                current_cost = new_cost
                if (new_cost < best_cost):
                    best = new_s
                    best_cost = new_cost
                    print best, best_cost
                    print T
            elif random.random() < math.exp(-(delta_cost / T)):
                current_s = new_s
                current_cost = new_cost
            M = M - 1
        time = time + Mo
        T = a * T
        Mo = b * Mo
    return best, best_cost

# returns a neighbor of the solution using random swapping
# find 2 routes in the solution with highest cost or 2 random routes
# randomly swap a node between them while under the capacity constaint


def neighbor(solution, capacity, customers):
    method = random.random()
    if method < 0.5:
        a, b = random.sample(solution.keys(), 2)
        route_a = solution.get(a)
        route_b = solution.get(b)
        node_a = random.choice(route_a[1:-1])
        node_b = random.choice(route_b[1:-1])

        # Swap
        route_a[route_a.index(node_a)] = node_b
        route_b[route_b.index(node_b)] = node_a

        # Randomly swap until a valid swap is found
        while not (valid(route_a, customers, capacity) and valid(route_b, customers, capacity)):
            route_a[route_a.index(node_b)] = node_a
            route_b[route_b.index(node_a)] = node_b
            a, b = random.sample(solution.keys(), 2)
            route_a = solution.get(a)
            route_b = solution.get(b)
            node_a = random.choice(route_a[1:-1])
            node_b = random.choice(route_b[1:-1])
            route_a[route_a.index(node_a)] = node_b
            route_b[route_b.index(node_b)] = node_a

    elif method >= 0.5:
        a, b = random.sample(solution.keys(), 2)
        route_a = solution.get(a)
        while len(route_a) <= 3:
            a, b = random.sample(solution.keys(), 2)
            route_a = solution.get(a)
        route_b = solution.get(b)
        node_a = random.choice(route_a[1:-1])

        # Random insert
        random_insert = random.randrange(1, len(route_b), 1)
        route_b.insert(random_insert, node_a)
        index = route_a.index(node_a)
        route_a.remove(node_a)

        # Randomly insert until a valid insert is found
        while not (valid(route_a, customers, capacity) and valid(route_b, customers, capacity)):
            route_b.remove(node_a)
            route_a.insert(index, node_a)
            a, b = random.sample(solution.keys(), 2)
            route_a = solution.get(a)
            while len(route_a) <= 3:
                a, b = random.sample(solution.keys(), 2)
                route_a = solution.get(a)
            route_b = solution.get(b)
            node_a = random.choice(route_a[1:-1])
            random_insert = random.randrange(1, len(route_b), 1)
            route_b.insert(random_insert, node_a)
            index = route_a.index(node_a)
            route_a.remove(node_a)

    # print "before ", solution
    # print "routea ", a, route_a, valid(route_a, customers, capacity)
    # print "routeb ", b, route_b, valid(route_b, customers, capacity)
    solution[a] = route_a
    solution[b] = route_b
    # print "after ", solution
    # for i in solution.values():
    #   print valid(i, customers, capacity)
    return solution


def valid(route, customers, capacity):
    total = 0
    for c in route:
        total += customers.get(c)
    return total <= capacity


# solution - hashmap of routes {route #: route}
# coordinates - hashmap of coordinates {node 1: (x,y)}
# return: total cost of solution


def cost(solution, coordinates):
    total_cost = 0
    for route in solution.values():
        current = 0
        next = 1
        while next < len(route):
            node1 = coordinates.get(route[current])
            node2 = coordinates.get(route[next])
            total_cost += euclid_distance(node1[0],
                                          node1[1], node2[0], node2[1])
            current = next
            next += 1
    return total_cost


def euclid_distance(x1, y1, x2, y2):
    return float(math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2)))

'''
cust = {1: 0, 2: 3, 3: 9, 4: 6, 5: 5,
        6: 7, 7: 12, 8: 15, 9: 3}
loc = {0: (0, 0), 1: (82, 76), 2: (96, 44), 3: (50, 5), 4: (49, 8),
       5: (13, 7), 6: (29, 89), 7: (58, 30), 8: (84, 39), 9: (14, 24)}

i = initialSolution(cust, 15)
print cost(i, loc)
'''
instances = os.listdir(".\A-VRP")
'''
for instance in instances:
    nodes, vehicles, capacity, coordinates, customers, optimal = parser(
        ".\A-VRP\\" + instance)
# print coordinates
# print customers
    best, best_cost = annealingCVRP(customers, capacity, coordinates, 10000)
    print "Instance: ", instance
    print "Best solution: ", best
    print "Best cost: ", best_cost
    print "Optimal cost: ", optimal
'''
nodes, vehicles, capacity, coordinates, customers, optimal = parser(
    ".\A-VRP\\" + instances[1])

best, best_cost = annealingCVRP(customers, capacity, coordinates, 100000)
print "Best solution: ", best
print "Best cost: ", best_cost
print "Optimal cost: ", optimal


'''
print customers

s = initialSolution(customers, capacity)

print s

print neighbor(s, 100)

'''
'''
print coordinates
print cost(s, coordinates)
'''
# print capacity
# print valid([1, 14, 9, 28, 26, 2, 22, 20, 12, 19, 11, 31, 13, 21, 30, 4,
# 18, 10, 3, 23, 6, 27, 1], customers, capacity)

test = {1: [1, 25, 7, 20, 12, 19, 32, 1],
        2: [1, 3, 21, 5, 13, 11, 33, 8, 1],
        3: [1, 31, 26, 28, 6, 27, 9, 14, 1],
        4: [1, 23, 24, 29, 30, 2, 15, 22, 1],
        5: [1, 16, 17, 4, 10, 18, 1]}
print cost(test, coordinates)
