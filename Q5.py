'''
Annealing CVRP()

'''
import math
import random
import os
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
            if i == 5:
                capacity = int(''.join(c for c in line if c.isdigit()))
            if i >= 7 and i < 7 + nodes:
                a = line.split()
                coordinates[int(a[0])] = int(a[1]), int(a[2])
            if i > 7 + nodes and i <= 7 + 2 * nodes:
                a = line.split()
                customers[int(a[0])] = int(a[1])

    return nodes, vehicles, capacity, coordinates, customers

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
    print s
    a = 0.85  # temp reduction multiplier
    b = 1.05  # iteration multiplier
    Mo = 5  # time to next param update
    best = s
    T = 5000
    current_s = s
    current_cost = cost(s, coordinates)
    print current_cost
    best_cost = current_cost
    time = 0
    while time < maxT and T >= 0.001:
        M = Mo
        while (M >= 0):
            new_s = neighbor(current_s, capacity)
            new_cost = cost(new_s, coordinates)
            delta_cost = new_cost - current_cost
            if delta_cost < 0:
                current_s = new_s
                current_cost = cost(new_s, coordinates)  # ???
                if (new_cost < best_cost):
                    best = new_s
                    best_cost = cost(best, coordinates)  # ???
            elif random.random() < math.exp(-delta_cost / T):
                current_s = new_s
                current_cost = cost(current_s, coordinates)  # ???
            M = M - 1
        time = time + Mo
        T = a * T
        Mo = b * Mo
    return best, best_cost

# returns a neighbor of the solution using random swapping
# find 2 routes in the solution with highest cost or 2 random routes
# randomly swap a node between them while under the capacity constaint


def neighbor(solution, capacity):

    method = random.random()

    if method < 0.5:
        a, b = random.sample(solution.keys(), 2)
        route_a = solution.get(a)
        route_b = solution.get(b)
        print "route a", route_a
        print "route b", route_b
        node_a = random.choice(route_a[1:-1])
        node_b = random.choice(route_b[1:-1])

        # Swap
        route_a[route_a.index(node_a)] = node_b
        route_b[route_b.index(node_b)] = node_a

        # Randomly swap until a valid swap is found
        while not valid(route_a, customers, capacity) and not valid(route_b, customers, capacity):
            a, b = random.sample(solution.keys(), 2)
            route_a = solution.get(a)
            route_b = solution.get(b)
            node_a = random.choice(route_a[1:-1])
            node_b = random.choice(route_b[1:-1])
            route_a[route_a.index(node_a)] = node_b
            route_b[route_b.index(node_b)] = node_a

    else:
        a, b = random.sample(solution.keys(), 2)
        route_a = solution.get(a)

        while len(route_a) <= 4:
            a, b = random.sample(solution.keys(), 2)
            route_a = solution.get(a)
        route_b = solution.get(b)
        node_a = random.choice(route_a[1:-1])

        # Append
        random_insert = random.randrange(1, len(route_b), 1)
        route_b.insert(random_insert, node_a)
        route_a.remove(node_a)

        # Randomly append until a valid append is found
        while not valid(route_b, customers, capacity):
            a, b = random.sample(solution.keys(), 2)
            route_a = solution.get(a)
            route_b = solution.get(b)
            print "route a", route_a
            print "route b", route_b
            node_a = random.choice(route_a[1:-1])
            random_insert = random.randrange(1, len(route_b), 1)
            route_b.insert(random_insert, node_a)
            route_a.remove(node_a)

    solution[a] = route_a
    solution[b] = route_b

    return solution


def valid(route, customers, capacity):
    total = 0
    for c in route:
        total += customers.get(c)
    return total < capacity


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
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

'''
cust = {1: 0, 2: 3, 3: 9, 4: 6, 5: 5,
        6: 7, 7: 12, 8: 15, 9: 3}
loc = {0: (0, 0), 1: (82, 76), 2: (96, 44), 3: (50, 5), 4: (49, 8),
       5: (13, 7), 6: (29, 89), 7: (58, 30), 8: (84, 39), 9: (14, 24)}

i = initialSolution(cust, 15)
print cost(i, loc)
'''

nodes, vehicles, capacity, coordinates, customers = parser(
    ".\A-VRP\A-n32-k5.vrp")

best, best_cost = annealingCVRP(customers, capacity, coordinates, 10000)

print best
print best_cost
print cost(best, coordinates)


'''
print customers

s = initialSolution(customers, capacity)

print s

print neighbor(s, 100)

'''
'''
print coordinates
print cost(s, coordinates)


test = {1: [1, 22, 32, 20, 18, 14, 8, 27, 1],
        2: [1, 13, 2, 17, 31, 1],
        3: [1, 28, 25, 1],
        4: [1, 30, 19, 9, 10, 23, 16, 11, 26, 6, 21, 1],
        5: [1, 15, 29, 12, 5, 24, 4, 3, 7, 1]}
print cost(test, coordinates)
'''
