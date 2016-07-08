'''
Annealing CVRP()
{ S0 = Initial solution
 = 0.99
  = 1.05
M0 = 5
BestS = Best solution T = 5000
CurrentS = S0
CurrentCost = Cost(CurrentS) BestCost = Cost(BestS)
Time = 0
do {M = M0
do {
NewS = Neighbor(CurrentS); NewCost=Cost(NewS)
 Cost = NewCost   CurrentCost If ( Cost < 0)
CurrentS=NewS CurrentCost=Cost(CurrentS); If (NewCost < BestCost) then
BestS=NewS
BestCost = Cost(BestS)
   Cost
else if (Random < e T then
CurrentS=NewS
CurrentCost = Cost(CurrentS); M=M 1
//Temperature reduction multiplier // Iteration multiplier
//Time until next parameter update
 } while (M   0) Time = Time + M0; T =T;
M0 = M0;
} while (Time > MaxTime and T > 0.001);
Return(BestS);
}
'''
import math
import random
# Parser
# return hashmap of capacity for each node, list of customers, hashmap of
# coordinates for each node


# customers - array of tuples (customer, demand)
# return: hashmap of routes {route #: route}

def initialSolution(customers, capacity):
    solution = {}
    visited = []
    while len(visited) != len(customers):
        c = capacity
        route = [0]
        for customer in customers:
            if customer[1] <= c and customer[0] not in visited:
                route.append(customer[0])
                visited.append(customer[0])
                c -= customer[1]
        route.append(0)
        solution[len(solution)] = route
    return solution


def annealingCVRP(customers, capacity, vehicles, coordinates, maxT):
    s = initialSolution(customers, capacity)
    a = 0.99  # temp reduction multiplier
    b = 1.05  # iteration multiplier
    Mo = 5  # time to next param update
    best = s
    T = 5000
    current_s = s
    current_cost = cost(s)
    time = 0
    while time < maxT and T > 0.001:
        M = Mo
        while (M > 0):
            new_s = neighbor(s)
            new_cost = cost(new_s, coordinates)
            delta_cost = new_cost - current_cost
            if delta_cost < 0:
                current_s = new_s
                current_cost = new_cost
                if (new_cost < best_cost):
                    best = new_s
                    best_cost = new_cost
            elif random.random() < math.exp(-delta_cost / T):
                current_s = new_s
                current_cost = new_cost
            M = M - 1
        time = time + Mo
        T = a * T
        Mo = b * Mo
    return best

# returns a neighbor of the solution using random swapping


def neighbor(solution, capacity):

	# find 2 routes in the solution with highest cost or 2 random routes
	# randomly swap a node between them while under the capacity constaint
	neighbor = solution  # don't think we need this assignment...
	a, b = random.sample(neighbor.keys(), 2)
	route_a = neighbor.get(a)
	route_b = neighbor.get(b)
	node_a = random.choice(route_a)
	node_b = random.choice(route_b)

	# Swap
	route_a[route_a.index(node_a)] = node_b
	route_b[route_b.index(node_b)] = node_a

	# Need checking here to see if the swap is valid (i.e. route is within capacity)
	# if swapping not valid, select another route randomly

	neighbor[a] = route_a
	neighbor[b] = route_b

    return neighbor

def valid(route, customers, capacity):
	return True


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

cust = [(1, 0), (2, 3), (3, 9), (4, 6), (5, 5), (6, 7), (7, 12), (8, 15), (9, 3)]
loc = {0: (0, 0), 1: (82, 76), 2: (96, 44), 3: (50, 5), 4: (49, 8),
       5: (13, 7), 6: (29, 89), 7: (58, 30), 8: (84, 39), 9: (14, 24)}

s = initialSolution(cust, 15)

print cost(s, loc)
