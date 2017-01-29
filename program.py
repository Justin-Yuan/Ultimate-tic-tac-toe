import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

import time 

global winScores		#how much we are winning each board by (9 element array) from 0 to 1 (0.5 = tie)
global prScores			#how much we want to win each board (9 element array) from 0 to 1 

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
	for i in range(nextsquare*9, nextsquare*10):
		if squares[i].value == 0: #Square must be empty
		vm.append(nextsquare*9 + i)
	return vm

for i in range(nextsquare*9,nextsquare*10): 
				squares.append(square(i-2,data[i]))

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
	if boardWinner(board)!= 0
		return 0;
	if isBoardFull(board).............

def updateScores(game, player):
	for i in range (0, 8):
		if winScores[i]!=0 and winScores[i]!=1:
			winScores[i] = winScore(game[i*9, i*10])
	

def get_move(timeout, data):

	game = data([2:83]


	if (time < changeAlgTime):

		PLAYER=data[0]
		nextsquare=data[1]

		#if going first
		if gameJustStarted():
			return 40


		if nextsquare != 9:

			#getting valid moves
			for i in range(nextsquare*9,nextsquare*10): 
				squares.append(square(i-2,data[i]))
			vm = findValidMoves(squares, nextsquare)


			#cheesing



		else:

	else:









	




