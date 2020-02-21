import numpy as np

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

def valid(board, pos, num):
    """
    board: the current board
    position: the position to be filled in. a tuple (row, column) 
    num: the number you would put in the given position. could be either 0 or 1
    """
    ### Board characteristics

    side = len(board)
    row, col = pos
    cnt_lmt = side/2
    
    temp = np.copy(board)   
    temp[row, col] = num
    
    ### Row condition: no three same numbers next to each other allowed
    chk_left_limit = max(0, col-2)
    chk_right_limit = min(side-3, col) # not inclusive   
    
    # loop through the starting position of the three consecutive elements
    for cl in range(chk_left_limit, chk_right_limit + 1):
        if temp[row, cl] == temp[row, cl + 1 ] == temp[row, cl + 2 ]:
            print(row,cl)
            print("Three consecutive fail - Row")
            return False
    
    
    ### Number of elements check - column
    # only need to check if the submitted number is valid. no need to care about the other number
    elem_cnt = (temp[:, col] == num).sum()
    if elem_cnt > cnt_lmt:
            print("Number of Elements Fail - Column")
            return False
    
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
