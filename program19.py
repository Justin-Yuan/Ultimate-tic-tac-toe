import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import time
from copy import deepcopy

global winScores		#how much we are winning each board by (9 element array) from 0 to 1 (0.5 = tie)
global prScores			#how much we prioritize each board (9 element array) from 0 to 1 
global gameStage		#how many moves have passed
global threshold		#algorithm shift after gameStage > threshold

# positive and negative infinity 
posinf = 999999
neginf = -999999

# define weights for different squares when evaluating the utility function 
weights = []

class square:
	def __init__(self,ID,val):
		self.ID = ID
		self.value = val
		self.bigSq = self._getbigSq()
		self.smallSq = self._getsmallSq()
	def _getbigSq(self):
		#return 3*int(self.ID/27) + int((self.ID%9)/3)
		return int(self.ID/9)
	def _getsmallSq(self):
		return self.ID%9

def findValidMoves(squares,nextsquare): 
	vm = []
	if nextsquare != 9:
		for i in range(nextsquare*9, nextsquare*9+9): #I changed the bound, plz double check 
			if squares[i].value == 0: #Square must be empty
			vm.append(i)	
	else:
		for i in range(81):
			if squares[i].value == 0: #Square must be empty
				if isBoardWon(getBigBoard(squares,squares[i].bigSq))==0: #Can't play in a won board
					if not isBoardFull(getBigBoard(squares,squares[i].bigSq)): #Can't play in a full board
						vm.append(i)
	return vm


def boardWinner(squares):
	#Input: squares = 8 item list of squares 
	#Output: 0 if not win, 1 if 1 won, 2 if 2 won
	def compareSquares(squares,s1,s2,s3,v):
		if squares[s1]==squares[s2] and squares[s1]==squares[s3] and squares[s1]==v:
			return True
		else:
			return False
	if compareSquares(squares,0,1,2,1): return 1
	if compareSquares(squares,0,1,2,2): return 2
	if compareSquares(squares,3,4,5,1): return 1
	if compareSquares(squares,3,4,5,2): return 2
	if compareSquares(squares,6,7,8,1): return 1
	if compareSquares(squares,6,7,8,2): return 2
	if compareSquares(squares,0,3,6,1): return 1
	if compareSquares(squares,0,3,6,2): return 2
	if compareSquares(squares,1,4,7,1): return 1
	if compareSquares(squares,1,4,7,2): return 2
	if compareSquares(squares,2,5,8,1): return 1
	if compareSquares(squares,2,5,8,2): return 2
	if compareSquares(squares,0,4,8,1): return 1
	if compareSquares(squares,0,4,8,2): return 2
	if compareSquares(squares,2,4,6,1): return 1
	if compareSquares(squares,2,4,6,2): return 2
	return 0

def isBoardFull(squares):
	for i in range(9):
		if squares[i]==0:
			return False
	return True

def isBoardEmpty(squares):
	for i in range(9):
		if squares[i]!=0:
			return False
	return True

def getBigBoard(squares,bigSq):
	sq = []
	for i in range(81):
		if squares[i].bigSq == bigSq:
			sq.append(squares[i].value)
	return sq

def winScore(board, player):

	if boardWinner(board)==player:
		return 1;
	if boardWinner(board)!= 0:
		return 0;
	if isBoardFull(board):
		return 0.5;

	#insert algorithm for calculating win score of one small board




def updateScores(game, player):
	for i in range (0, 8):
		if winScores[i]!=0 and winScores[i]!=1:
			winScores[i] = winScore(game[i*9 : i*10])

	#algorithm for updating prScores 
	
####################################################################################
# minimax + alpha-beta pruninng helper functions 

def alpha_beta(state, depth=6):
	v = max_value(state, neginf, posinf, depth)
	return 

def max_value(state, alpha, beta, depth):
	if terminal(depth):
		return utility(state)
	v = neginf
	for move in successors(state):
		v = max(v, min_value(result(state, move), alpha, beta, depth-1))
		if v >= beta:
			return v 
		alpha = max(alpha, v)
	return v

def min_value(state, alpha, beta, depth):
	if terminal(depth):
		return utility(state)
	v = posinf
	for move in successors(state):
		v = min(v, max_value(result(state, move), alpha, beta, depth-1))
		if v <= alpha:
			return v
		beta = min(beta, v)
	return v

def utility(state):
	# use the weights array to evaluate a score for the winning condition 
	return ... 

def terminal(depth):
	# determines the ending condition for the recursion 
	if depth == 0:
		return True 
	else:
		return False 


def result(state, move):
	# return the new state after trying a testing move
	stateCopy = deepcopy(state) 
	stateCopy[move+2] = state[0]	# update the move 
	# update the next player
	if state[0] == 1:
		stateCopy[0] == 2
	else:
		stateCopy[0] == 1
	# update the nextsquare 
	stateCopy[1] = square(move, state[]).bigSq
	return stateCopy


def successors(state):
	# return a list of numbers representing all posible moves 
	squares = []
	nextsquare = state[1]
	for i in range(2,83): 
		squares.append(square(i-2,state[i]))
	return findValidMoves(squares, nextsquare)
	
####################################################################################

def get_move(timeout, data):

	startTime = time.clock()
	game = data[2:83]

	if gameJustStarted():
			return 40
			
	# put valid moves and nextsqure here 

	if (gameStage < threshold): #algorithm 1 (denial of diagonals)

		PLAYER=data[0]
		nextsquare=data[1]

		#if going first
		


		if nextsquare != 9:

			#getting valid moves
			for i in range(nextsquare*9,nextsquare*10): 
				squares.append(square(i-2,data[i]))
			vm = findValidMoves(squares, nextsquare)





		else: #free move
			for i in range(2,83): 
				squares.append(square(i-2,data[i]))
			vm = findValidMoves(squares,nextsquare)

	else: #algorithm 2 (with deeper searching)

		return alpha-beta(game)







