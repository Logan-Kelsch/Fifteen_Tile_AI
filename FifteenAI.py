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
#personal function file
from funcs_AI import *
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
           [9, 10, 11, 12],\
           [0, 13, 14, 15]]
  return board

#game class
class game15(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('15 GAME - Logan Kelsch')
    self.setGeometry(400, 400, W_WIDTH,W_HEIGHT)
    self.__moveNum = 0 #tally of move numbers
    self.__complete = False #bool for game completion
    self.__board = setBoard() #board values (2D array)
    #self.show()
    # Create a QTimer to repeatedly call the simulate_click method
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.algo_click)
    self.timer.start(20) #milliseconds

 #               oldest            newest
  last_moves = []
  moves_tracked = 3
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
    qp.drawText(170,75,str(getBoardScore(self.__board)))
    
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