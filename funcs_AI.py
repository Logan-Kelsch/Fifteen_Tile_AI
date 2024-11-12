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

#will score current board to tell how close it is
def getBoardScore(some_board):
    score = 0
    return score

#will be used with decision fringe to return board
#returning a board so it will be scored amongst other moves
def getThinkingBoard(some_board, some_move):
    board = []
    return board

#will return a set of moves that can be made from current board
#these moves will be individually thrown into getthinkingboard,getboardscore
#to gather which move is best
def getDecisionFringe(some_board):
    fringe = []#should be dict or tuple of move:score
    return fringe

#this will take decisionfringe, make thinkingboard of each decision,
#get score for each thinkingboard/decision, and then return the best decision
def getBestMove(some_decision_fringe, some_board):
    move = 0
    return move

def makeBestMove(some_best_move):
    #do something
    return