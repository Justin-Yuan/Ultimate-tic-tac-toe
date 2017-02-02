# import pycuda.driver as cuda
# import pycuda.autoinit
# from pycuda.compiler import SourceModule
import time
from copy import deepcopy

global gameStage	#how many moves have passed
winScores = [0, 0, 0, 0, 0, 0, 0, 0, 0]		#how close we are to winning a board (9 element array) from -1 to 1 (0 = tie)
weights = [0.5, 0, 0.5, 0, 1, 0, 0.5, 0, 0.5]	#how much we prioritize each board (9 element array) from 0 to 1 
# define weights for different squares when evaluating the utility function 

gameStage = 0		#number of moves since start of game
threshold = 45		#algorithm shift after gameStage > threshold

# positive and negative infinity 
posinf = 999999
neginf = -999999

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
		for i in range(9):
			if squares[i].value == 0: #Square must be empty
				vm.append(nextsquare*9 + i)
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

def opponent(player):
	if player == 1:
		return 2
	return 1

def numPieces(board, player):
	sum = 0
	for i in range(9):
		sum += (board[i] == player)
	return sum

def winScore(board, player):
	if boardWinner(board)==player:
		return 1
	if boardWinner(board)!= 0
		return -1
	if isBoardFull(board)
		return 0
	score = 0
	opp = opponent(player)

	#three in a row across centre
	if board[4] == player: #centre is player
		for i in range(4):
			if board[i] == player or board[8-i] == player: 
				score += 1

	elif board[4] == 0: #centre is empty
		i = 0
		while(i<4):
			if board[i] == opp or board[8-i] == opp:
				continue
			elif board[i] == player and board[8-i] == player:
				score = 1
				i = 4
			elif board[i] == player or board[8-i] == player:
				score += 0.3
			i++

	else: #centre is opponent
		for i in range(4):
			if board[i] == player or board[8-i] == player:
				continue
			elif board[i] == opp or board[8-i] == opp:
				score += -1

	#three in a row that do not intersect centre
	if board[0] == 0 or board[1] == 0 or board[2] == 0:
		score += (((board[0]==player + board[1]==player + board[2]==player) - (board[0]==opp + board[1]==opp + board[2]==opp)))/2
	if board[0] == 0 or board[3] == 0 or board[6] == 0:
		score += (((board[0]==player + board[3]==player + board[6]==player) - (board[0]==opp + board[3]==opp + board[6]==opp)))/2
	if board[2] == 0 or board[5] == 0 or board[8] == 0:
		score += (((board[2]==player + board[5]==player + board[8]==player) - (board[2]==opp + board[5]==opp + board[8]==opp)))/2
	if board[6] == 0 or board[7] == 0 or board[8] == 0:
		score += (((board[6]==player + board[7]==player + board[8]==player) - (board[6]==opp + board[7]==opp + board[8]==opp)))/2

	#normalize scores
	score = score/2
	if score >= 1
		score = 1
	if score <= -1
		score = -1
	return score

def updateScores(game, player):
	for i in range (9):
		if winScores[i]!=-1 and winScores[i]!=1:
			winScores[i] = winScore(game[i*9:i*9+9])
	
	weights[0] = max(winScores[1]+winScores[2], winScores[3]+winScores[6], winScores[4]+winScores[8])+abs(min(winScores[1]+winScores[2], winScores[3]+winScores[6], winScores[4]+winScores[8]))
	# if weights[1] != 0:
	# 	weights[1] = max((winScores[0]+winScores[2])/2, (winScores[4]+winScores[7])/2)+abs(min((winScores[0]+winScores[2])/2, (winScores[4]+winScores[7])/2))
	weights[2] = max(winScores[1]+winScores[0], winScores[5]+winScores[8], winScores[4]+winScores[8])+abs(min(winScores[1]+winScores[2], winScores[3]+winScores[6], winScores[4]+winScores[8]))
	# if weights[3] != 0:
	# 	weights[3] = max((winScores[0]+winScores[6])/2, (winScores[4]+winScores[5])/2)+abs(min((winScores[0]+winScores[6])/2, (winScores[4]+winScores[5])/2))
	weights[4] = 1
	# if weights[5] != 0:
	# 	weights[5] = max((winScores[2]+winScores[8])/2, (winScores[4]+winScores[3])/2)+abs(min((winScores[2]+winScores[8])/2, (winScores[4]+winScores[3])/2))
	weights[6] = max(winScores[0]+winScores[3], winScores[2]+winScores[4], winScores[7]+winScores[8])+abs(min(winScores[0]+winScores[3], winScores[2]+winScores[4], winScores[7]+winScores[8]))
	# if weights[7] != 0:
	# 	weights[7] = max((winScores[1]+winScores[4])/2, (winScores[6]+winScores[8])/2)+abs(min((winScores[1]+winScores[4])/2, (winScores[6]+winScores[8])/2))
	weights[8] = max(winScores[2]+winScores[5], winScores[0]+winScores[4], winScores[6]+winScores[7])+abs(min(winScores[2]+winScores[5], winScores[0]+winScores[4], winScores[6]+winScores[7]))
	
	for j in range (9):
		if winScores[j] == -1 or winScores[j] == 1:
			weights[j] = 1
	return

####################################################################################
# minimax + alpha-beta pruninng helper functions 

def alpha_beta(timeout, state, depth=6):
	timeStart = time.clock()
	v, nextMove = max_value(timeStart, timeStart+timeout, state, neginf, posinf, depth)
	return nextMove


def max_value(timeStart, timeEnd, state, alpha, beta, depth):
	if abs(timeEnd - timeStart) < 0.0001:
		return -1, -1
	if terminal(depth):
		return utility(state), -1
	v = neginf
	for move in successors(state):
		tempMove = -1
		temp, tempMove = min_value(time.clock(), timeEnd, result(state, move), alpha, beta, depth-1)[0], move
		if temp == -1:
			break
		if v < temp: 
			v = temp
			nextMove = tempMove
		# v = max(v, temp)
		if v >= beta:
			return v, nextMove
		alpha = max(alpha, v)
	return v, nextMove


def min_value(timeStart, timeEnd, state, alpha, beta, depth):
	if abs(timeEnd - timeStart) < 0.0001:
		return -1, -1
	if terminal(depth):
		return utility(state), -1
	v = posinf
	for move in successors(state):
		tempMove = -1
		temp, tempMove = max_value(time.clock(), timeEnd, result(state, move), alpha, beta, depth-1)[0], move
		if temp == -1:
			break
		if v > temp:
			v = temp
			nextMove = tempMove
		# v = min(v, temp)
		if v <= alpha:
			return v, nextMove
		beta = min(beta, v)
	return v, nextMove


def utility(state):
	# use the weights array to evaluate a score for the winning condition
	temp_weights = deepcopy(weights)
	temp_winScores = deepcopy(winScores)
	updateScores(state, state[1])

	sum = 0
	for i in range(9):
		sum += weights[i]*winScores[i]
	weights = temp_weights
	winScores = temp_winScores

	return sum


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
	for i in range(nextsquare*9, nextsquare*9+9): 
		squares.append(square(i,state[i+2]))
	return findValidMoves(squares, nextsquare)

####################################################################################

def get_move(timeout, data):

	startTime = time.clock() 
	game = data[2:83]

	#if going first
	if gameStage == 0:
		return 37

	PLAYER=data[0]
	nextsquare=data[1]

	updateScores(game, PLAYER)

	if (gameStage < threshold): #algorithm 1 (denial of diagonals)
		gameStage += 1

		#prioritizing board to force opponent onto
		topLeftNum = numPieces(game[0:9], PLAYER)
		topRightNum = numPieces(game[18:27], PLAYER)
		botLeftNum = numPieces(game[54:63], PLAYER)
		botRightNum = numPieces(game[72:81], PLAYER)
		top = topLeftNum+topRightNum
		left = topLeftNum+botLeftNum
		right = topRightNum+botRightNum
		bot = botRightNum+botLeftNum
		num = [top, left, right, bot].sort()
		bias = []
		for i in range(4):
			if num[i] == top:
				bias.append(1)
			elif num[i] == bot:
				bias.append(7)
			elif num[i] == left:
				bias.append(3)
			else:
				bias.append(5)

		if nextsquare != 9:

			#getting valid moves
			for i in range(nextsquare*9,nextsquare*9+9): 
				squares.append(square(i,data[i+2]))
			vm = findValidMoves(squares,nextsquare)
			for temp in bias:
				square = nextsquare*9+temp
				if square in vm:
					if !isBoardWon(game[(square%9)*9, (square%9)*9+9]): # square%9 = board on which we want opponent to go
						return square
			temp = [topRightNum, topLeftNum, botLeftNum, botRightNum]
			while (len(temp)>0):
					choice = min(temp)
				if chioce == topRightNum and !isBoardWon(game[18:27]):
					return 2
				elif choice == topLeftNum and !isBoardWon(game[0:9]):
					return 0
				elif choice == botRightNum and !isBoardWon(game[72:81]):
					return 8
				elif !isBoardWon(game[54:63])
					return 6
				temp.remove(min(temp))
			return nextsquare*9+4


		else: #free move
			for i in range(2,83):
				squares.append(square(i,data[i+2]))
			vm = findValidMoves(squares,nextsquare)
			choice = weights.index(max(weights))
			if !isBoardWon(game[choice*9:choice*9+9]):
				for i in range (4):
					if !isBoardWon(game[bias[i]*9:bias[i]*9+9]):
						return bias[i]

	else: #algorithm 2 (with deeper searching)
		gameStage += 1
		return alpha_beta(timeout, data, 6)


