#ECE457A Assignment 1 Q2

#Evaluation Function 1: each board state is evaluated by the number of possible moves available to the player making the move (maximizing)
#Evaluation Function 2: each board state is evaluated by the number of possible moves available to the opposing player (minimizing)


class Player():
	def __init__ (self, player):
		self.player = player
		self.opponent = 1 if player == 2 else 2

	def makeMove(self, board, initial, next):
	"""Updates board with player move from initial tile [x1,y1] in direction of next tile [x2,y2]"""
		x_initial = initial[1]
		y_initial = initial[0]
		x_next = next[1]
		y_next = next[0]
	
		dx = x_next - x_initial
		dy = y_next - y_initial
	
		if not self.isValid(board, x_initial, y_initial, dx, dy):
			raise Exception("Invalid move for player " + str(self.player))
	
		while x_next < 4 and x_next >= 0 and y_next < 4 and y_next >= 0 and board.amount[y_initial][x_initial] > 0:
			board.occupied[y_next][x_next] = self.player
			#If next tile is invalid, move all remaining stones from initial tile to current tile
			if not self.isValid(board, x_next, y_next, dx, dy):
				board.amount[y_next][x_next] += board.amount[y_initial][x_initial]
				board.amount[y_initial][x_initial] = 0
			else:	
				board.amount[y_next][x_next] += 1
				board.amount[y_initial][x_initial] -= 1
			x_next = x_next + dx
			y_next = y_next + dy
		board.occupied[y_initial][x_initial] = 0


	def isValid(board, x_initial, y_initial, dx, dy):
	"""Returns whether a move from the intial tile in direction of next tile is valid"""

		if board.lastMove == self.player:
			return False

		if abs(dx) != 1 or abs(dy) != 1:
			return False

		#Check if next tile is occupied by opponent 
		if board.occupied[y_initial+dy][x_initial+dx] == self.opponent:
			return False

		#Check if next tile is outside of board range
		if x_initial+dx > len(board) or x_initial+dx < 0 or y_initial+dy > len(board) or y_initial+dy < 0:
			return False

		return True

class Board():
	def __init__(self):

		#Initialize 4x4 board
		self.occupied = [[0 for x in xrange(4)] for y in xrange(4)]
		self.amount = [[0 for x in xrange(4)] for y in xrange(4)]
		self.lastMove = None 

		#Starting positions and values for player 1 (top left corner) and player 2 (bottom right corner)
		self.occupied[0][0] = 1
		self.amount[0][0] = 10
		self.occupied[3][3] = 2
		self.amount[3][3] = 10

	def showBoard(self):
		print " ___________ ___________ ___________ ___________"
		for y in xrange(len(self.occupied)):
			print "|           |           |           |           |"
			row = ""
			for x in xrange(len(self.occupied[0])):
				row += "    {0} ({1})   ".format(self.amount[y][x],self.occupied[y][x])
			print row
			print "|___________|___________|___________|___________|"





