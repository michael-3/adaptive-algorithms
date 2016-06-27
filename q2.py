#ECE457A Assignment 1 Q2

#Evaluation Function 1: each board state is evaluated by the number of possible moves available to the player making the move (maximizing)
#Evaluation Function 2: each board state is evaluated by the number of possible moves available to the opposing player (minimizing)

class Agent():
	def __init__ (self, player, evalfunc):
		self.player = player
		self.evalfunc = evalfunc
		self.opponent = 1 if player == 0 else 1
	





