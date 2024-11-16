'''
    ATTENTION:
        THIS FILE IS OFFICIALLY DEPRICATED
        ALL FUNCTIONS HERE WERE MOVED INTO 
        THE FIFTEENAI.PY FILE FOR EASE OF
        ASSIGNMENT UPLOADING.
'''

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