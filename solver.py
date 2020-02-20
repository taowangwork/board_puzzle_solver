board = [
    [9, 0, 9, 9, 0, 9],
    [0, 9, 9, 0, 9, 1],
    [0, 1, 9, 9, 9, 0],
    [9, 0, 0, 9, 0, 9],
    [0, 9, 1, 0, 9, 0],
    [1, 9, 9, 9, 0, 0]
]
print(board)
pos = (3,3)
num = 0

def valid(board, pos, num):
    """
    board: the current board
    position: the position to be filled in. a tuple (row, column) 
    num: the number you would put in the given position. could be either 0 or 1
    """
    temp = board[:]
    side = len(board)
    row, col = pos
    temp[row][col] = num
    ### Row condition: no three same numbers in a row
    col_left_limit = max(0, col-2)
    col_right_limit = min(side,col+1)
    
    for st in range(col_left_limit, col_right_limit):
        if temp[row][st] == temp[row][st + 1 ] == temp[row][st + 2 ]:
            return False
    return True
    
    row_top_limit = max(0, row-2)
    row_bottom_limit = min(side,row+1)
    for st in range(row_top_limit, row_bottom_limit):
        if temp[col][st] == temp[col][st + 1 ] == temp[col][st + 2 ]:
            return False
    return True                  
    
valid(board, pos, num)   
