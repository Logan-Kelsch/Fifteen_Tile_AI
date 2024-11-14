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

#will score current board to tell how close it is
#calculate manhattan distance
def getBoardScore(board):
    score = 0
    boardVal = 0
    rLoc, cLoc = 0, 0
    manOffset = 0
    for r in range(4):
       for c in range(4):
          boardVal = board[r][c]
          if(boardVal!=0):
            rLoc = ((boardVal-1)//4)
            cLoc = ((boardVal-1)%4)
            manOffset = np.square(rLoc-r) + abs(cLoc-c)
          else:
            rLoc = 3
            cLoc = 3
            manOffset = abs(3-r) + abs(3-c)
          score += manOffset
    #score+=inversionCount(board)
    return score

def inversionCount(board):
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
    moveFringe = getMoveFringe(board, last_moves)
    fringeScores = []
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
    for move in moveFringe:
        tmpBoard = getThinkingBoard(board,move[0],move[1])
        last_moves_lookahead = copy.deepcopy(last_moves)
        last_moves_lookahead.pop(0)
        last_moves_lookahead.append(move)
        nextMove0, nextMove1 = getBestMove(tmpBoard, last_moves_lookahead)
        tmpBoard2 = getThinkingBoard(tmpBoard, nextMove0, nextMove1)
        
        fringeScores.append(getBoardScore(tmpBoard2))
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