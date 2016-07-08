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

# customers - array of tuples (customer, demand)


def initialSolution(customers, capacity):
    routes = []
    visited = []
    while len(visited) != len(customers):
        c = capacity
        route = [0]
        for customer in customers:
            if customer[1] <= c and customer[0] not in visited:
                route.append(customer[0])
                visited.append(customer[0])
                c -= customer[1]
        routes += route
    return routes

cust = [(2, 3), (3, 9), (4, 6), (5, 5), (6, 7), (7, 12), (8, 15), (9, 3)]

print initialSolution(cust, 15)
