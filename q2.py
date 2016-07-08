# ECE457A Assignment 1 Q2

# Evaluation Function 1:
# Each board state is evaluated by the number of possible moves available
# to the player making the move (maximizing)
# Evaluation Function 2:
# Each board state is evaluated by the number of possible moves available
# to the opposing player (minimizing)

import copy
import random
import math


class Player():

    def __init__(self, player):
        self.player = player
        self.opponent = 1 if player == 2 else 2

    def makeMove(self, board, initial, next, player):
        """	Updates board with player move from
                initial tile [x1,y1] in direction of next tile [x2,y2]
        """

        x_initial = initial[0]
        y_initial = initial[1]
        x_next = next[0]
        y_next = next[1]

        dx = x_next - x_initial
        dy = y_next - y_initial

        if not self.isValid(board, x_initial, y_initial, dx, dy, player):
            raise Exception("Invalid move for player " + str(player))

        stonesRemoved = 1

        while board.amount[y_initial][x_initial] > 0:
            board.occupied[y_next][x_next] = player
            # If next tile is invalid, move all remaining stones from initial
            # tile to current tile
            if (not self.isValid(board, x_next, y_next, dx, dy, player) or
                    stonesRemoved > board.amount[y_initial][x_initial]):
                board.amount[y_next][
                    x_next] += board.amount[y_initial][x_initial]
                board.amount[y_initial][x_initial] = 0
            else:
                board.amount[y_next][x_next] += stonesRemoved
                board.amount[y_initial][x_initial] -= stonesRemoved

            stonesRemoved += 1
            x_next += dx
            y_next += dy

        board.occupied[y_initial][x_initial] = 0
        board.lastMove = player

    def isValid(self, board, x_initial, y_initial, dx, dy, player):
        """
        Returns whether a move from the intial tile
        in direction of next tile is valid

        """

        if board.lastMove == player:
            return False

        if abs(dx) != 1 and abs(dy) != 1:
            return False

        # Check if next tile is outside of board range
        if (x_initial + dx > 3 or x_initial + dx < 0 or
                y_initial + dy > 3 or y_initial + dy < 0):
            return False

        # Check if currrent tile is occupied by player
        if board.occupied[y_initial][x_initial] != player:
            return False

        # Check if next tile is free
        if (board.occupied[y_initial + dy][x_initial + dx] != 0 and
                board.occupied[y_initial + dy][x_initial + dx] != player):
            return False

        return True


class Node():

    def __init__(self, state, player):
        self.alpha = -float('inf')
        self.beta = float('inf')
        self.children = []
        self.state = state
        self.player = player
        self.best_move = None


class Agent(Player):

    def __init__(self, player, eval):
        Player.__init__(self, player)
        self.prev = ([0, 0], [0, 0])
        self.eval = eval
        self.moves = [(1, 0), (-1, 0), (0, -1), (0, 1),
                      (1, -1), (1, 1), (-1, -1), (-1, 1)]

    def makeBestMove(self, board, depth, prune):
        """Plays the best possibe move using min/max strategy"""

        # Build game tree
        root = Node(board, self.player)
        value = self.buildGameTree(depth, root, prune)
        if root.best_move[0] == self.prev[1] and root.best_move[1] == self.prev[0]:
            self.makeRndMove(board, 1)
        else:
            self.makeMove(board, root.best_move[
                0], root.best_move[1], self.player)
            nodes = self.getChildren(root)
            print "Searched " + str(nodes) + " nodes up to depth " + str(depth)
            print "Best move is move from " + str(root.best_move[0]) + " to " + str(root.best_move[1])
            self.prev = root.best_move

    def getChildren(self, node, container=[]):
        for c in node.children:
            container.append(c)
            if hasattr(c, 'children'):
                self.getChildren(c, container)
        return len(container)

    def buildGameTree(self, depth, root, prune, alpha=-float('inf'), beta=float('inf')):
        """Builds and searches the game tree recursively"""

        tiles = self.getPlayerTiles(root.state, root.player)
        all_moves = []
        opponent = 2 if root.player == 1 else 1

        # Get all possible moves from player
        for tile in tiles:
            possible_moves = self.movesFromTile(root.state, tile)
            for move in possible_moves:
                all_moves.append((tile, move))

        # Find heuristic value of leaf nodes based on evaluation function
        if depth == 0 or len(possible_moves) == 0:
            return self.calculateHeuristic(root.state)
        # Alpha-Beta Pruning
        if root.player == self.player:
            for move in all_moves:
                next_state = copy.deepcopy(root.state)
                self.makeMove(next_state, move[0], move[1], root.player)
                child = Node(next_state, opponent)
                value = self.buildGameTree(
                    depth - 1, child, prune, alpha, beta)
                if value > alpha:
                    alpha = value
                    root.best_move = (move[0], move[1])
                if alpha > beta and prune:
                    break
                root.children.append(child)
            return alpha
        else:
            for move in all_moves:
                next_state = copy.deepcopy(root.state)
                self.makeMove(next_state, move[0], move[1], root.player)
                child = Node(next_state, opponent)
                value = self.buildGameTree(
                    depth - 1, child, prune, alpha, beta)
                if value < beta:
                    beta = value
                    root.best_move = (move[0], move[1])
                if beta < alpha and prune:
                    break
                root.children.append(child)
            return beta

        # return root.alpha if root.player == self.player else root.beta

    def buildGameTree2(self, depth, root):
        """Builds and searches the game tree recursively"""

        tiles = self.getPlayerTiles(root.state, root.player)
        opponent = 2 if root.player == 1 else 1

        for tile in tiles:
            possible_moves = self.movesFromTile(root.state, tile)
            # Find heuristic value of leaf nodes based on evaluation function
            if depth == 0 or len(possible_moves) == 0:
                root.value = self.calculateHeuristic(root.state)
                return root.value
            for move in possible_moves:
                next_state = copy.deepcopy(root.state)
                self.makeMove(next_state, tile, move, root.player)
                child = Node(next_state, opponent)
                value = self.buildGameTree(depth - 1, child)
                # Alpha-Beta Pruning
                if root.player == self.player:
                    if value > root.alpha:
                        root.alpha = value
                        root.best_move = (tile, move)
                    if root.alpha > root.beta:
                        # return root.alpha
                        break
                else:
                    if value < root.beta:
                        root.beta = value
                        root.best_move = (tile, move)
                    if root.beta < root.alpha:
                        # return root.beta
                        break
                root.children.append(child)

        return root.alpha if root.player == self.player else root.beta

    def calculateHeuristic(self, state):
        # Find the number of moves available to player
        if self.eval == 1:
            return self.numberOfMoves(state, self.player) - self.numberOfMoves(state, self.opponent)
        if self.eval == 2:
            return 1 / math.exp(self.numberOfMoves(state, self.opponent))

    def makeRndMove(self, board, seed):
        """Plays a random valid move"""

        all_moves = []
        tiles = self.getPlayerTiles(b, self.player)
        for tile in tiles:
            moves = self.movesFromTile(b, tile)
            for move in moves:
                all_moves.append((tile, move))
        if not all_moves:
            raise Exception("No moves to play!")
        else:
            random_move = random.choice(all_moves)
            self.makeMove(b, random_move[0], random_move[1], self.player)
            print "Random move from " + str(random_move[0]) + " to " + str(random_move[1])

    def movesFromTile(self, board, tile):
        """Returns the possible moves a player can make from tile"""

        if board.occupied[tile[1]][tile[0]] == 0:
            raise Exception("No tile on " + str(tile))

        possible_moves = []

        for move in self.moves:
            if self.isValid(board, tile[0], tile[1], move[0], move[1], board.occupied[tile[1]][tile[0]]):
                possible_moves.append((tile[0] + move[0], tile[1] + move[1]))

        return possible_moves

    def numberOfMoves(self, board, player):
        """Returns the number of moves that can made by player"""

        tiles = self.getPlayerTiles(board, player)
        numberOfMoves = 0

        for tile in tiles:
            for move in self.moves:
                if self.isValid(board, tile[0], tile[1], move[0], move[1], player):
                    numberOfMoves += 1

        return numberOfMoves

    def getPlayerTiles(self, board, player):
        """Returns the tiles owned by player"""

        tiles = []

        for y in xrange(len(board.occupied)):
            for x in xrange(len(board.occupied[0])):
                if board.occupied[y][x] == player:
                    tiles.append((x, y))

        return tiles


class Board():

    def __init__(self):

        # Initialize 4x4 board
        self.occupied = [[0 for x in xrange(4)] for y in xrange(4)]
        self.amount = [[0 for x in xrange(4)] for y in xrange(4)]
        self.lastMove = None

        # Starting positions and values for player 1 (top left corner) and
        # player 2 (bottom right corner)
        self.occupied[0][0] = 1
        self.amount[0][0] = 10
        self.occupied[3][3] = 2
        self.amount[3][3] = 10

    def show(self):
        print " ___________ ___________ ___________ ___________"
        for y in xrange(len(self.occupied)):
            print "|           |           |           |           |"
            row = ""
            for x in xrange(len(self.occupied[0])):
                row += "    {0} ({1})   ".format(
                    self.amount[y][x], self.occupied[y][x])
            print row
            print "|___________|___________|___________|___________|"


# Simulate AI agent vs random agent
total = 0
games = 10
for runs in xrange(games):
    b = Board()
    p1 = Agent(1, 0)
    p2 = Agent(2, 1)
    print "Game Start"
    b.show()
    turn = 1
    while True:
        print "Turn " + str(turn)
        print "Player One Move"
        p1.makeRndMove(b, 1)
        # b.show()
        if p2.numberOfMoves(b, 2) == 0:
            print "GAME OVER"
            break
        print "Player Two Move"
        p2.makeBestMove(b, 3, True)
        # b.show()
        if p1.numberOfMoves(b, 1) == 0:
            print "GAME OVER"
            break
        turn += 1
        # if turn > 50:
        #   break
    print "Total turns for AI to beta Random in game " + str(runs) + ": " + str(turn)
    total += turn
print "Average moves: ", total / games


# Show searches with and without pruning
b2 = Board()
p3 = Agent(1, 0)
p4 = Agent(2, 1)
print "Pruning Enabled"
p3.makeMove(b2, [0, 0], [1, 0], 1)
b2.show()
p4.makeBestMove(b2, 3, True)
b2 = Board()
print "Pruning Disabled"
p3.makeMove(b2, [0, 0], [1, 0], 1)
b2.show()
p4.makeBestMove(b2, 3, False)
