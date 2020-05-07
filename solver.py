import numpy as np

### The board only allows 0 and 1
board = [
    [9, 0, 9, 9, 0, 9],
    [0, 9, 9, 0, 9, 1],
    [0, 1, 9, 9, 9, 0],
    [9, 0, 0, 9, 0, 9],
    [0, 9, 1, 0, 9, 0],
    [1, 9, 9, 9, 0, 0]
]

board = np.array(board)
print(board)
pos = (1,1)
num = 0

# class alolboard():
#     def __init__(self, board):
#         self.board = board
        
#### Given the current board. Check if putting the proposed number in the proposed location would violate any rules of the game. 
def valid(board, pos, num):
    """
    board: the current board, 0 and 1 are the positions are filled out. 9 represent empty squares
    position: the position to be filled in. a tuple (row, column) 
    num: the number you would put in the given position. could be either 0 or 1
    """
    ### Board characteristics

    side = len(board)
    row, col = pos
    cnt_lmt = side/2
    
    temp = np.copy(board)   
    temp[row, col] = num
    
    ###########################
    #### Rule 1: no three same numbers next to each other. both column and row
    ###########################
    ### Row condition: no three same numbers next to each other allowed
    chk_left_limit = max(0, col-2)
    chk_right_limit = min(side-3, col) # not inclusive   
    
    # loop through the starting position of the three consecutive elements
    for cl in range(chk_left_limit, chk_right_limit + 1):
        if temp[row, cl] == temp[row, cl + 1 ] == temp[row, cl + 2 ]:
            print(row,cl)
            print("Three consecutive fail - Row")
            return False
    
    ###########################
    #### Rule 2: Each row and column must have the same number of 0s and 1s
    ###########################
        
    ### Number of elements check - column
    # only need to check if the submitted number is valid. no need to care about the other number
    elem_cnt = (temp[:, col] == num).sum()
    if elem_cnt > cnt_lmt:
            print("Number of Elements Fail - Column")
            return False
        
    ###########################
    #### Rule 3: No identical rows or columns
    ###########################    
    ### Repeating column check
    for stcl in range(0, side-1):
        for cl in range(stcl+1, side):
            print(stcl, cl)
            if (temp[:, stcl] == temp[:, cl]).all():
                print(stcl, cl)
                return False
            
    ### if passes all the checks then valid
    return True
              
    
valid(board, pos, num)    


#### Check the next open position on the board row by row. Also very importantly, return True when the game is over, i.e. no more open positions.
def next_open(board):
    side = len(board)
    for row in range(side):
        for col in range(side):
            if board[row, col] not in [0,1]:
                return (row, col)
    return True




### The main part of the code: depth first search (DFS)
### recursive    
def solve(board):
    ###
    ### end condition
    if next_open(board) == True:
        return True
    else:
        ### next position 
        row, col = next_open(board)
    
    for num in range(2):
        ### update board
        board[row, col] = num
        
        ### Check if the updated board satisfy the rules
        if valid(board, (row, col), num) == True:
            ### recursively solve the current updated board
            ### if the current guess is valid, then return True. This will happen when we reach the end of the board.
            if solve(board) == True:
                return True
    ### after going through all the guesses and not going into the next level, meaning the current board does not have any valid solution.
    ### reset the board and return False. return back to the previous level.
    board[row, col] = 9
    
    return False