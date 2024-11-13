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

#will score current board to tell how close it is
#calculate manhattan distance
def getBoardScore(board):
    score = 0
    boardVal = 0
    rLoc, cLoc = 0, 0
    for r in range(4):
       for c in range(4):
          boardVal = board[r][c]
          rLoc = 3 - (boardVal//4)
          cLoc = 3 - (boardVal%4)
          score += abs(rLoc-r) + abs(cLoc-c)
    return score
'''
#will score current board to tell how close it is
#calculate manhattan distance
def getBoardScore(board):
    score = 0
    flatBoard = []
    for i in range(0,16):
       flatBoard.append(board[i])
          
    return score
'''
#will be used with decision fringe to return board
#returning a board so it will be scored amongst other moves
def getThinkingBoard(board, r, c):
    e_r, e_c = getEmptySquare(board)
    thinkingBoard = makeMove(board, r, c, e_r, e_c)
    return thinkingBoard

#will return a set of moves that can be made from current board
#these moves will be individually thrown into getthinkingboard,getboardscore
#to gather which move is best
def getMoveFringe(board):
    e_r, e_c = getEmptySquare(board)

    possibleMoves = [[0,0], [0,1], [0,2], [0,3],\
                     [1,0], [1,1], [1,2], [1,3],\
                     [2,0], [2,1], [2,2], [2,3],\
                     [3,0], [3,1], [3,2], [3,3]]
    fringe = []
    for move in possibleMoves:
       if(isValidMove(4, move[0], move[1], e_r, e_c)):
          fringe.append(move)
       
    return fringe

#this will take decisionfringe, make thinkingboard of each decision,
#get score for each thinkingboard/decision, and then return the best decision
def getBestMove(board):
    moveFringe = getMoveFringe(board)
    fringeScores = []
    for move in moveFringe:
       fringeScores.append(getBoardScore(getThinkingBoard(board,move[0],move[1])))
    bestMoveLoc = np.argmin(fringeScores)
    b_r = moveFringe[bestMoveLoc][0]
    b_c = moveFringe[bestMoveLoc][1]

    b_r = (b_r+1)*100
    b_c = (b_c+1)*100

    return b_r, b_c

def getBestMove_depth4(board):
    mFringe_d1 = getMoveFringe(board)
    fringeScore_1 = []
    
    
    
    
    
    
    bestMovesFrom_2 = []
    for move in mFringe_d1:
        tmpBoard_for2 = getThinkingBoard(board, move[0], move[1])
        mFringe_d2 = getMoveFringe(tmpBoard_for2)
        fringeScore_2 = []
        bestMovesFrom_3 = []
        for move_2 in mFringe_d2:
            tmpBoard_for3 = getThinkingBoard(tmpBoard_for2, move_2[0], move_2[1])
            mFringe_d3 = getMoveFringe(tmpBoard_for3)
            fringeScore_3 = []
            bestMovesFrom_4 = []
            for move_3 in mFringe_d3:
                tmpBoard_for4 = getThinkingBoard(tmpBoard_for3, move_3[0], move_3[1])
                mFringe_d4 = getMoveFringe(tmpBoard_for3)
                fringeScore_4 = []

                for move_4 in mFringe_d4:
                   fringeScore_4.append(getBoardScore(getThinkingBoard(tmpBoard_for4, move_4[0], move_4[1])))
                #fringeScore_3.append(getBoardScore(getThinkingBoard(tmpBoard_for3, move_3[0], move_3[1])))
                bestMovesFrom_4.append(np.min(fringeScore_4))#one for each mFringe_d3
            #fringeScore_2.append(getBoardScore(getThinkingBoard(tmpBoard_for2, move_2[0], move_2[1])))
            bestMovesFrom_3.append(np.min(bestMovesFrom_4))#one for each mFringe_d2
        #fringeScore_1.append(getBoardScore(getThinkingBoard(board, move[0], move[1])))
        bestMovesFrom_2.append(np.min(bestMovesFrom_3))#as many as mFringe_d1
    bestMoveLoc = np.argmin(bestMovesFrom_2)
    b_r = mFringe_d1[bestMoveLoc][0]
    b_c = mFringe_d1[bestMoveLoc][1]

    b_r = (b_r+1)*100
    b_c = (b_c+1)*100

    return b_r, b_c

def makeMove(board, row, col, e_r, e_c):
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
          board[row][c] = board[row][c+dir]
        board[row][col] = 0
    #adjacency of column, meaning cells will shift up or down
    #same code as just above flipped, refer to comments above for explanation
    if(col==e_c):
        dir = 0
        if(row<e_r):
          dir = -1
        else:
          dir = 1
        for r in range(e_r,row,dir):
          board[r][col] = board[r+dir][col]
        board[row][col] = 0
    return board

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