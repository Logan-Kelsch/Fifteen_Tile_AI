#COSC 411 Homework 1
#15 game with AI
#Logan Kelsch

'''
	In this assignment , we took the code that we created for the 15 tile project and were asked to add
	an algorithmic bot, based off of the A* algorithm, that is designed to solve the puzzle.
'''

#IMPORTS
import sys
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication
import random
#IMPORTS FOR AI
from PyQt5.QtTest import QTest
from PyQt5.QtCore import QTimer, QPoint
import numpy as np
import copy

#4x4 GRID, window size 600x600, grid square sizes of 100x100
CELL_COUNT = 4
CELL_SIZE = 100
GRID_ORIGINX = 100
GRID_ORIGINY = 100
W_WIDTH = 600
W_HEIGHT = 600

#function made specifically for ease of calling in game initiation
#creates random and solvable game board
def setBoard():
		#create list of board values to ensure solvability before putting it into a 2d array
		boardVals = list(range(0,16))
		beatable = False
		#while loop for ensuring solvability
		while(beatable == False):
			#shuffle 0-15 values in list
			random.shuffle(boardVals)
			#variable for total inversion tallies
			inversions = 0
			#for all values in list except final, as comparison involves a +1 function
			for i in range(0,15):
				#set first value in iteration as inversion comparison value, iterate down list
				crntVal = boardVals[i]
				#for each value further down the board than crntVal
				for j in range(i+1,15):
					#value for ease of data access
					compVal = boardVals[j]
					#if inversion needs to be tallied
					if(crntVal>compVal):
						inversions+=1
			#finding odd/even property of row empty square is on
			emptyLoc = (boardVals.index(0)//4)%2
			#considering conditions for solvable board,
			#mod 2 of inversions and empty square row must not be equal
			if((inversions%2)!=emptyLoc):
				beatable = True
		#making empty board
		board = [[0 for _ in range(4)] for _ in range(4)]
		#insert solvable board values
		for i in range(0,16):
			board[i//4][i%4] = boardVals[i]
		#return solvable board
		return board

#BEGINNING OF ALL FUNCTIONS OUTSIDE OF THE CLASS
#GAME CLASS BEGINS ON LINE 400
#___________________________________________________________________

#function takes the provided scoring method and outputs the given board's score
def getBoardScore(board):
	score = score_topHalfSolver(board)
	return score

#function detects whether or not top row was solved
#all references to chunks are functions that are explained at line #96
def firstRowSolved(board):
		if(solved_chunk1(board) and solved_chunk2(board)):
						return True
		else:
						return False

#function detects whether or not second from top row was solved
def secondRowSolved(board):
		if(solved_chunk3(board) and solved_chunk4(board)):
						return True
		else:
						return False

#function collects whether or not top two rows were solved
def topHalfSolved(board):
		if(firstRowSolved(board) and secondRowSolved(board)):
				return True
		else:
				return False

'''
	Chunks were used to make the heuristic function and scoring system more digestable
	by the model, considering my attempt was based off of a limited depth seeking algorithm

	solved_chunk functions return whether or not sets of tiles have been solved
'''
#function detects whether or not 1-2 are solved
def solved_chunk1(board):
		if(board[0][0]==1 and board[0][1]==2): 
				return True
		else:
				return False
#function detects whether or not 3-4 are solved
def solved_chunk2(board):
		if(board[0][2]==3 and board[0][3]==4):
				return True
		else:
				return False
#function detects whether or not 5-6 are solved
def solved_chunk3(board):
		if(board[1][0]==5 and board[1][1]==6):
				return True
		else:
				return False
#function detects whether or not 7-8 are solved
def solved_chunk4(board):
		if(board[1][2]==7 and board[1][3]==8):
				return True
		else:
				return False
#function detects whether or not 9 and 13 are solved
#I picked this set as this is the natural direction of solving the puzzle
def solved_chunk5(board):
		if(board[2][0]==9 and board[3][0]==13):
				return True
		else:
				return False

#this function was designed to punish the score of a board where the pieces are placed
#in reverse order, I added this as the limited depth makes fixing these flips impossible
def score_punishCases(board):
		score = 0
		if(not solved_chunk1(board)):
				if(board[0][0]!=1 and board[0][1]==2):
						score+=40
		elif(not solved_chunk2(board)):
				if(board[0][2]==3 and board[0][3]!=4 and board[0][3]!=0):
						score+=40
				if(board[0][2]!=3 and board[0][3]==4 and board[0][2]!=0):
						score+=40
				if(board[1][2]==3 and board[1][3]==4):
						score+=40
				if(board[2][2]==3 and board[2][3]==4):
						score+=40
		elif(not solved_chunk3(board)):
				if(board[1][0]!=5 and board[1][1]==6):
						score+=40
		elif(not solved_chunk4(board)):
				if(board[1][2]==7 and board[1][3]!=8 and board[1][3]!=0):
						score+=40
				if(board[1][2]!=7 and board[1][3]==8 and board[1][2]!=0):
						score+=40
				if(board[1][2]!=0 and board[1][3]==8 and board[2][2]==7):
						score+=40
				if(board[2][2]==7 and board[2][3]==8):
						score+=40
				if(board[3][2]==7 and board[3][3]==8):
						score+=40
		return score
	
#this is my custom heuristic function that solved chunks in order
#I added a linear handicap for each chunk, to ensure that the 
#algorithm solves them in order
def score_topHalfSolver(board):
		score = 0
		if(not topHalfSolved(board)):
				if(not firstRowSolved(board)):
						if(not solved_chunk1(board)):
								score += score_boardEval(board, [1,2])
								score += 100 #example of chunk handicap
						else:#chunk 2 not solved
								score += score_boardEval(board, [3,4])
								score += 80
				else:#second row is not solved
						if(not solved_chunk3(board)):
								score += score_boardEval(board, [5,6])
								score += 60
						else:#chunk 4 not solved
								score += score_boardEval(board, [7,8])
								score += 40
		else:#second half not solved
				if(not solved_chunk5(board)):
						score += score_boardEval(board, [9,13])
						score+=20
				else:
					return score_Manhattan(board)
		#handicap addition to avoid pitfalls
		score += score_punishCases(board)
		return score

#simple function to run around the board and score it based off the requested numbers to score
def score_boardEval(board, values):
	score = 0
	#for all board locations
	for r in range(4):
		for c in range(4):
			#if this board value is one to be scored
			if(board[r][c] in values):
				score += calc_indivManhattan(board[r][c], r, c)
	return score


#will score current board to tell how close it is
#to proper location
#calculate manhattan distance
def score_Manhattan(board):
		score = 0
		#for all board locations
		for r in range(4):
			 for c in range(4):
					score += calc_indivManhattan(board[r][c], r, c)
		return score

#given the tile value and the current location
#calculates perfect location and manhattan distance
def calc_indivManhattan(boardVal, r, c):
		rLoc = ((boardVal-1)//4)#correct row
		cLoc = ((boardVal-1)%4)#correct col
		return (abs(rLoc-r) + abs(cLoc-c))

#depricated function used to output the number of inversions
#this is done by flattening the board into an array and tallying
def score_Inversions(board):
		invs = 0
		flatBoard = []
		#for each board tile
		for i in range(0,16):
				flatBoard.append(board[i//4][i%4])
		#for each flat board tile
		for i in range(0,16):
				crntVal = flatBoard[i]
				#using bubble method to count inversions
				for j in range(i+1,16):
					tmpVal = flatBoard[j]
					if(crntVal>tmpVal and crntVal!=0):
							invs+=1
		return invs

#this function creates a board simulation
#will be used with decision fringe to return board
#returning a board so it will be scored amongst other moves
def getThinkingBoard(board, r, c):
		e_r, e_c = getEmptySquare(board)
		thinkingBoard = makeMove(board, r, c, e_r, e_c)
		return thinkingBoard

#will return a set of moves that can be made from current board
#these moves will be individually thrown into getthinkingboard,getboardscore
#to gather which move is best
def getMoveFringe(board, last_moves):
		#collect empty cell location
		e_r, e_c = getEmptySquare(board)
		#array of possible moves for ease of calculation
		possibleMoves = [[0,0], [0,1], [0,2], [0,3],\
										 [1,0], [1,1], [1,2], [1,3],\
										 [2,0], [2,1], [2,2], [2,3],\
										 [3,0], [3,1], [3,2], [3,3]]
		fringe = []
		#for each move that can be made in the entire game
		for move in possibleMoves:
			 #if it is valid
			 if(isValidMove(4, move[0], move[1], e_r, e_c)):
					#and if it is not a recent move
					if(isRecentMove(move,last_moves) is False):
						fringe.append(move)
		return fringe

#this return whether or not the move was of the last last_moves array
def isRecentMove(move, last_moves):
	#for each last move from array
	for lmoves in last_moves:
			if(lmoves[0]==move[0] and lmoves[1]==move[1]):
					return True
	return False

#this will take decisionfringe, make thinkingboard of each decision,
#get score for each thinkingboard/decision, and then return the best decision
#I did not comment the function as it is now DEPRICATED
def getBestMove(board, last_moves):
		moveFringe = getMoveFringe(board, last_moves)
		fringeScores = []
		for move in moveFringe:
			tmpBoard = getThinkingBoard(board,move[0],move[1])
			fringeScores.append(getBoardScore(tmpBoard))
		bestMoveLoc = np.argmin(fringeScores)
		b_r = moveFringe[bestMoveLoc][0]
		b_c = moveFringe[bestMoveLoc][1]
		print(f'move to make: {b_r} {b_c}')
		return b_r, b_c

'''
	This function is the function used in the current code to calculate the next best move
	for the bot.
	This function creates a move-tree with depth of 4. It checks all possible moves from this range,
	and then grabs the best move from each direction,
	TO CALCULATE ONLY!!!!!! the best following move.

	This allows for maximum versatility under having only a move depth of 4
'''
def getBestMove_d4(board, last_moves):
		#collect all moves possible from current REAL board
		moveFringe = getMoveFringe(board, last_moves)
		#array that holds the score for each best move path
		fringeScores = []
		#for each move possible
		for move in moveFringe:
				#create an imaginary board to create a branch of moves from
				tmpBoard = getThinkingBoard(board,move[0],move[1])
				#create a new set of recent moves to ensure these paths
				#contain no looping
				last_moves_lookahead = copy.deepcopy(last_moves)
				last_moves_lookahead.pop(0)
				last_moves_lookahead.append(move)
				#create a new move fringe for a secondary move from the real board
				moveFringe_2 = getMoveFringe(tmpBoard,last_moves_lookahead)
				#array to hold scores of each second move
				fringeScores_2 = []
				#add this move to the list to consider if a closer good shorter move exists
				fringeScores_2.append(getBoardScore(tmpBoard))
				#from here this process will repeat in extact same form, I will leave one comment
				#at the deepest of the looping to explain what happens at the leaves
				for move2 in moveFringe_2:
						tmpBoard2 = getThinkingBoard(tmpBoard,move2[0],move2[1])
						last_moves_lookahead_2 = copy.deepcopy(last_moves_lookahead)
						last_moves_lookahead_2.pop(0)
						last_moves_lookahead_2.append(move2)
						moveFringe_3 = getMoveFringe(tmpBoard2,last_moves_lookahead_2)
						fringeScores_3 = []
						fringeScores_3.append(getBoardScore(tmpBoard2))
						for move3 in moveFringe_3:
								tmpBoard3 = getThinkingBoard(tmpBoard2, move3[0], move3[1])
								last_moves_lookahead_3 = copy.deepcopy(last_moves_lookahead_2)
								last_moves_lookahead_3.pop(0)
								last_moves_lookahead_3.append(move3)
								moveFringe_4 = getMoveFringe(tmpBoard3,last_moves_lookahead_3)
								fringeScores_4 = []
								fringeScores_4.append(getBoardScore(tmpBoard3))
								for move4 in moveFringe_4:
										#in this loop we are looking at each move that can be taken that is
										#four moves from the original board
										#this scores array is collecting seperately for each third move array
										tmpBoard4 = getThinkingBoard(tmpBoard3, move4[0], move4[1])
										fringeScores_4.append(getBoardScore(tmpBoard4))
								#the best score is grabbed from each 4 move board
								fringeScores_3.append(np.min(fringeScores_4))
						#the bst score is grabbed from each 3 move board
						fringeScores_2.append(np.min(fringeScores_3))
				#the best score is grabbed from each 2 move board
				fringeScores.append(np.min(fringeScores_2))
		#the location of the best tree in the fringe of current moves
		#is obtained
		bestMoveLoc = np.argmin(fringeScores)
		#a best (b_) row and col click move is grabbed
		b_r = moveFringe[bestMoveLoc][0]
		b_c = moveFringe[bestMoveLoc][1]
		#and returned as the best move
		return b_r, b_c

#this function is unchanged and swaps the boards values according to the move made
def makeMove(board, row, col, e_r, e_c):
		newboard = copy.deepcopy(board)
		if(row==e_r):
				#direction variable for value shift optimization
				#0 dir value does not apply unless empty square is clicked
				dir = 0
				#if true, this statement suggests player clicked in adjacent row and to the left of empty square
				if(col<e_c):
					dir = -1 #will shift TO THE RIGHT
				else:
					dir = 1 #will shift TO THE LEFT
				#for cells in adjacent row, between clicked cell and empty cell
				for c in range(e_c,col,dir):
					#PULL cell values towards empty spot down the line, and assign zero to clicked square accordingly
					newboard[row][c] = newboard[row][c+dir]
				newboard[row][col] = 0
		#adjacency of column, meaning cells will shift up or down
		#same code as just above flipped, refer to comments above for explanation
		if(col==e_c):
				dir = 0
				if(row<e_r):
					dir = -1
				else:
					dir = 1
				for r in range(e_r,row,dir):
					newboard[r][col] = newboard[r+dir][col]
				newboard[row][col] = 0
		return newboard

#this function returns the location of the empty tile location
#returns -1 -1 on error, only exists in custom boards
def getEmptySquare(board):
		for r in range(len(board)):
			for c in range(len(board[r])):
				if(board[r][c] == 0):
					return r, c
		return -1, -1

#function checks whether or not tiles can slide according to requested move
def isValidMove(CELL_COUNT, r, c, e_r, e_c):
		if (bool(r==e_r) != bool(c==e_c)):
			if (0<=r < CELL_COUNT and 0 <= c < CELL_COUNT):
				return 1
		else:
			return 0

#simply returns if the board has been completed
def isCompleteBoard(board):
	 #compare board with a perfect board
		completeBoard = [[0 for _ in range(4)] for _ in range(4)]
		#iterate through board to assign solved values to comparison board
		for i in range(0,16):
			completeBoard[i//4][i%4] = (i+1)%16
		#check for equivalence
		if(board == completeBoard):
			return True
		else:
			return False

#GAME CLASS
#___________________________________________________________________
#this class contains the algorithm click funcion
#					     paint board function
#						 and click -> action function
class game15(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('15 GAME - Logan Kelsch')
		self.setGeometry(400, 400, W_WIDTH,W_HEIGHT)
		self.__moveNum = 0 #tally of move numbers
		self.__complete = False #bool for game completion
		self.__complete_topHalf = False
		self.__board = setBoard() #board values (2D array)
		#creates a QTimer to repeatedly call the simulate_click method
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.algo_click)#connects function to timer
		self.timer.start(500) #milliseconds

	#holds moves in order from oldest to newest
	last_moves = []
	#length of moves that should be tracked to avoid looping
	moves_tracked = 5
	#creation of initial past moves, all NULL (-1,-1)
	for i in range(moves_tracked):
		last_moves.append([-1,-1])

	#function used for 
	def algo_click(self):
		#end timer, algo, and game if game is complete
		if self.__complete is True:
			self.timer.stop()
			return
		
		#gather best move data
		row, col = getBestMove_d4(self.__board, self.last_moves)
		#fix last moves according
		self.last_moves.pop(0)
		self.last_moves.append([row,col])

		#convert the proper move into x and y locations for simulated
		#screen clicking
		x = (col+1)*100
		y = (row+1)*100
		
		#this function simulates a mouse click
		QTest.mouseClick(self, Qt.LeftButton, pos=QPoint(x, y))

	#paint board
	def paintEvent(self, event):
		qp = QPainter()
		blackPen = QPen(QBrush(Qt.black),1)
		qp.begin(self)
		#clear background
		qp.fillRect(event.rect(),Qt.white)
		qp.setFont(QFont('Arial',40))
		#completion check, for drawtext."YOU WIN" and self.__complete
		complete = True
		#for each square in board
		for r in range(len(self.__board)):
			for c in range(len(self.__board[r])):
				#check for 0 or for appropriate baord values
				if(self.__board[r][c] != (r*4+c+1)):
					if(self.__board[r][c] != 0):
						complete = False
		#assign discovered completeness
		self.__complete = complete
		if(self.__complete == True):
			qp.drawText(170,75,'YOU WIN!')
		#move counter below board
		qp.drawText(320,550,str(self.__moveNum))
		qp.drawText(100,550,'MOVES:')
		
		qp.setPen(blackPen)
		#for each square in board, print lines, numbers, and fill colors
		for r in range(len(self.__board)):
			for c in range(len(self.__board[r])):
				#variable for ease of drawText function use
				currVal = self.__board[r][c]
				#color setting for nice gradient between variabes! Hand selected RGB values
				if(currVal!=0):
					qp.setBrush(QColor(255-currVal*16,255-currVal*8,255-currVal*6))
				else: #if empty square
					qp.setBrush(QColor(0,120,75))
				#draw cells
				qp.drawRect(GRID_ORIGINX + c * CELL_SIZE, GRID_ORIGINY + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
				if(self.__board[r][c]!=0): #if the cell has a number
					qp.drawText(GRID_ORIGINX + c * CELL_SIZE + 25, GRID_ORIGINY + r * CELL_SIZE + 75,str(self.__board[r][c]))
				if self.__board[r][c] == 0: #dont print any number if the number is zero, is empty cell
					continue
		qp.end()

	#per mouse click function
	def mousePressEvent(self, event):
		#do nothing if game is complete
		if self.__complete is True:
			return
		#collect mouse click location
		row = (event.y() - GRID_ORIGINY) // CELL_SIZE
		col = (event.x() - GRID_ORIGINX) // CELL_SIZE
		
		#collect empty cell information
		emptyRow, emptyCol = getEmptySquare(self.__board)
				
		#if mouse click is within bounds of board
		if isValidMove(CELL_COUNT, row, col, emptyRow, emptyCol):
			self.__moveNum+=1
			self.__board = makeMove(self.__board, row, col, emptyRow, emptyCol)

		#check to see if board is completely solved
		self.__complete = isCompleteBoard(self.__board)
		#finish mouseclick function, update board
		self.update()

#run program
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = game15()
	ex.show()
	sys.exit(app.exec_())