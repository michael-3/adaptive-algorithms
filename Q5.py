'''
Annealing CVRP()
{ S0 = Initial solution
 ↵ = 0.99
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
 } while (M   0) Time = Time + M0; T = ↵ ⇤T;
M0 = ⇤M0;
} while (Time > MaxTime and T > 0.001);
Return(BestS);
}
'''