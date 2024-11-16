#COSC 411 Homework 1
#15 game
#Logan Kelsch

#Initial structure of code imitated from tictactoe in-class example.
#most specifically, the initial CELL_COUNT, etc. variables! 
#More useful than any other concept I would have came up with

#IMPORTS
import sys
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication
import random

#IMPORTS FOR AI
#for simulating a mouse click
from PyQt5.QtTest import QTest
from PyQt5.QtCore import QTimer, QPoint
import numpy as np

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

def setBoardCustom():
  board = [[1, 2, 3, 4],\
           [5, 6, 7, 8],\
           [12, 10, 11, 9],\
           [14, 0, 13, 15]]
  return board


#___________________________________________________________________

#this is the function file for all new functions to the program
#that are implemented for this assignment

'''
Attempted method:

FUNCTIONS:
    - GATHER BOARD DATA, SCORE CURRENT BOARD POSITIONING
    - CREATE FRINGE OF POSSIBLE MOVES
    - COMPARE BOARD SCORES COMPLETELY, FRINGE AND CURRENT
    - - - CONSIDER MAKING A MULTI STEP DEPTH OF TREE
    - EXECUTE BOARD MOVE BASED OFF OF PREDICTION MADE
'''

import numpy as np
import copy

def getBoardScore(board):
   score = score_topHalfSolver(board)
   return score

def firstRowSolved(board):
    if(solved_chunk1(board) and solved_chunk2(board)):
            return True
    else:
            return False

def secondRowSolved(board):
    if(solved_chunk3(board) and solved_chunk4(board)):
            return True
    else:
            return False

def topHalfSolved(board):
    if(firstRowSolved(board) and secondRowSolved(board)):
        return True
    else:
        return False
    
def solved_chunk1(board):
    if(board[0][0]==1 and board[0][1]==2): 
        return True
    else:
        return False

def solved_chunk2(board):
    if(board[0][2]==3 and board[0][3]==4):
        return True
    else:
        return False

def solved_chunk3(board):
    if(board[1][0]==5 and board[1][1]==6):
        return True
    else:
        return False

def solved_chunk4(board):
    if(board[1][2]==7 and board[1][3]==8):
        return True
    else:
        return False
    
def solved_chunk5(board):
    if(board[2][0]==9 and board[3][0]==13):
        return True
    else:
        return False

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
   
def score_topHalfSolver(board):
    score = 0
    boardVal = 0
    rLoc, cLoc = 0, 0
    if(not topHalfSolved(board)):
        if(not firstRowSolved(board)):
            if(not solved_chunk1(board)):
                for r in range(4):
                    for c in range(4):
                        if(board[r][c]<3 and board[r][c]!=0):
                            score += calc_indivManhattan(board[r][c], r, c)
                score += 100
            else:#chunk 2 not solved
                for r in range(4):
                    for c in range(4):
                        if(board[r][c]<5 and board[r][c]>2):
                            score += calc_indivManhattan(board[r][c], r, c)
                score += 80
        else:#second row is not solved
            if(not solved_chunk3(board)):
                for r in range(4):
                    for c in range(4):
                        if(board[r][c]<7 and board[r][c]>4):
                            score += calc_indivManhattan(board[r][c], r, c)
                score += 60
            else:#chunk 4 not solved
                for r in range(4):
                    for c in range(4):
                        if(board[r][c]<9 and board[r][c]>6):
                            score += calc_indivManhattan(board[r][c], r, c)
                score += 40
    else:#second half not solved
        if(not solved_chunk5(board)):
            for r in range(4):
                for c in range(4):
                    if(board[r][c]==9 or board[r][c]==13):
                        score += calc_indivManhattan(board[r][c], r, c)
            score+=20
        
        return score_Manhattan(board)
    score += score_punishCases(board)
    return score

#will score current board to tell how close it is
#calculate manhattan distance
def score_Manhattan(board):
    score = 0
    for r in range(4):
       for c in range(4):
          if(board[r][c]!=0):
            score += calc_indivManhattan(board[r][c], r, c)
          else:
            score += calc_indivManhattan(board[r][c], r, c)
    return score

def calc_indivManhattan(boardVal, r, c):
    rLoc = ((boardVal-1)//4)
    cLoc = ((boardVal-1)%4)
    return (abs(rLoc-r) + abs(cLoc-c))

def score_Inversions(board):
    invs = 0
    flatBoard = []
    for i in range(0,16):
        flatBoard.append(board[i//4][i%4])
    for i in range(0,16):
        crntVal = flatBoard[i]
        for j in range(i+1,16):
           tmpVal = flatBoard[j]
           if(crntVal>tmpVal and crntVal!=0):
              invs+=1
    return invs
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
    e_r, e_c = getEmptySquare(board)
    possibleMoves = [[0,0], [0,1], [0,2], [0,3],\
                     [1,0], [1,1], [1,2], [1,3],\
                     [2,0], [2,1], [2,2], [2,3],\
                     [3,0], [3,1], [3,2], [3,3]]
    fringe = []
    for move in possibleMoves:
       if(isValidMove(4, move[0], move[1], e_r, e_c)):
          if(isRecentMove(move,last_moves) is False):
            fringe.append(move)
       
    return fringe

def isRecentMove(move, last_moves):
  for lmoves in last_moves:
      if(lmoves[0]==move[0] and lmoves[1]==move[1]):
          return True
  return False

#this will take decisionfringe, make thinkingboard of each decision,
#get score for each thinkingboard/decision, and then return the best decision
def getBestMove(board, last_moves):
    moveFringe = getMoveFringe(board, last_moves)
    fringeScores = []
    for move in moveFringe:
       tmpBoard = getThinkingBoard(board,move[0],move[1])
       fringeScores.append(getBoardScore(tmpBoard))
    bestMoveLoc = np.argmin(fringeScores)
    b_r = moveFringe[bestMoveLoc][0]
    b_c = moveFringe[bestMoveLoc][1]

    #b_r = (b_r+1)*100
    #b_c = (b_c+1)*100

    print(f'move to make: {b_r} {b_c}')
    return b_r, b_c

def getBestMove_d2(board, last_moves):
    #we have a fringe of moves
    #now instead of appending fringe scores and grabbing argmin
    #we want to make a move fringe specifically for each
    #  move in fringe
    #for each d2fringe we will have a new last_moves and board
    #we will then append and NOTargmin best scores for each fringe
    #instead we will have the regular min represent each fringe
    # so following each .min will not be var assignment
    #    it will be appending to lists of best scores alike
    #      fringescores in getBestMove. and then we will
    #        grab argmin to be able to pick out
    #            move from original moveFringe
    moveFringe = getMoveFringe(board, last_moves)
    fringeScores = []
    for move in moveFringe:
        tmpBoard = getThinkingBoard(board,move[0],move[1])
        last_moves_lookahead = copy.deepcopy(last_moves)
        last_moves_lookahead.pop(0)
        last_moves_lookahead.append(move)
        moveFringe_2 = getMoveFringe(tmpBoard,last_moves_lookahead)
        fringeScores_2 = []
        #add this move to the list to consider good shorter moves too
        fringeScores_2.append(getBoardScore(tmpBoard))
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
                    tmpBoard4 = getThinkingBoard(tmpBoard3, move4[0], move4[1])
                    fringeScores_4.append(getBoardScore(tmpBoard4))
                fringeScores_3.append(np.min(fringeScores_4))
            fringeScores_2.append(np.min(fringeScores_3))
        fringeScores.append(np.min(fringeScores_2))
    bestMoveLoc = np.argmin(fringeScores)
    b_r = moveFringe[bestMoveLoc][0]
    b_c = moveFringe[bestMoveLoc][1]

    #b_r = (b_r+1)*100
    #b_c = (b_c+1)*100

    print(f'move to make: {b_r} {b_c}')
    return b_r, b_c

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

def getEmptySquare(board):
    for r in range(len(board)):
      for c in range(len(board[r])):
        if(board[r][c] == 0):
          return r, c
    return -1, -1

def isValidMove(CELL_COUNT, r, c, e_r, e_c):
    if (bool(r==e_r) != bool(c==e_c)):
      if (0<=r < CELL_COUNT and 0 <= c < CELL_COUNT):
        return 1
    else:
      return 0
    
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

#___________________________________________________________________
#game class
class game15(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('15 GAME - Logan Kelsch')
    self.setGeometry(400, 400, W_WIDTH,W_HEIGHT)
    self.__moveNum = 0 #tally of move numbers
    self.__complete = False #bool for game completion
    self.__complete_topHalf = False
    self.__board = setBoard() #board values (2D array)
    #self.show()
    # Create a QTimer to repeatedly call the simulate_click method
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.algo_click)
    self.timer.start(10) #milliseconds

 #               oldest            newest
  last_moves = []
  moves_tracked = 5
  for i in range(moves_tracked):
    last_moves.append([-1,-1])

  

  def algo_click(self):
    #do nothing if game is complete
    if self.__complete is True:
      self.timer.stop()
      return
    

    
    row, col = getBestMove_d2(self.__board, self.last_moves)
    self.last_moves.pop(0)
    self.last_moves.append([row,col])
    '''
    if(self.__complete_topHalf==False and topHalfSolved(self.__board)\
       and solved_chunk5(self.__board)):
      for i in range(3,self.moves_tracked):
        self.last_moves.pop(0)
      self.__complete_topHalf= True
    '''

    x = (col+1)*100
    y = (row+1)*100
    print(f'move to make: [{row} {col}]')
    print(f'loc to click: [{x} {y}]')
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
    
    #collect location of empty cell
    for r in range(len(self.__board)):
      for c in range(len(self.__board[r])):
        if(self.__board[r][c] == 0):
          #empty cell row/col variables
          emptyRow = r
          emptyCol = c
          break
        
    #XOR function for determining if active game move is valid
    if(bool(row==emptyRow) != bool(col==emptyCol)):
      self.__moveNum+=1

    #if mouse click is within bounds of board
    if 0<=row < CELL_COUNT and 0 <= col < CELL_COUNT:
      #check for adjacency
      if(row==emptyRow):
        #direction variable for value shift optimization
        #0 dir value does not apply unless empty square is clicked
        dir = 0
        #if true, this statement suggests player clicked in adjacent row and to the left of empty square
        if(col<emptyCol):
          dir = -1 #will shift TO THE RIGHT
        else:
          dir = 1 #will shift TO THE LEFT
        #for cells in adjacent row, between clicked cell and empty cell
        for c in range(emptyCol,col,dir):
          #PULL cell values towards empty spot down the line, and assign zero to clicked square accordingly
          self.__board[row][c] = self.__board[row][c+dir]
        self.__board[row][col] = 0
      #adjacency of column, meaning cells will shift up or down
      #same code as just above flipped, refer to comments above for explanation
      if(col==emptyCol):
        dir = 0
        if(row<emptyRow):
          dir = -1
        else:
          dir = 1
        for r in range(emptyRow,row,dir):
          self.__board[r][col] = self.__board[r+dir][col]
        self.__board[row][col] = 0

    #compare board with a perfect board
    board = [[0 for _ in range(4)] for _ in range(4)]
    #iterate through board to assign solved values to comparison board
    for i in range(0,16):
      board[i//4][i%4] = (i+1)%16
    #check for equivalence
    if(self.__board == board):
      self.__complete = True
    #finish mouseclick function, update board
    self.update()
    #figure out what cell they clicked in
    #retrieve that cell from the board

#run program
if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = game15()
  ex.show()
  sys.exit(app.exec_())