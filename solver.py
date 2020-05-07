import numpy as np

### The board only allows 0 and 1
class alolboard():
    def __init__(self, board):
        self.board = board
        self.edge = len(board)
    
    ### compare if the two np arrays a and b are the same, conditioning on if both a and b does not contain unfilled numbers, i.e. 9
    def compare(self, a,b):
        if (a==9).any() or (b==9).any():
            return False
        else:
            ### return True if the two np arrays are the same
            return (a == b).all()
    
    #### Given the current board. Check if putting the proposed number in the proposed location would violate any rules of the game. 
    def valid(self, pos, num):
        """
        board: the current board, 0 and 1 are the positions are filled out. 9 represent empty squares
        position: the position to be filled in. a tuple (row, column) 
        num: the number you would put in the given position. could be either 0 or 1
        """
        ### Board characteristics
        row, col = pos
        cnt_lmt = self.edge/2
        
        temp = np.copy(self.board)   
        temp[row, col] = num
        
        ###########################
        #### Rule 1: no three same numbers next to each other. both column and row
        ###########################
        ### Row condition: no three same numbers next to each other allowed
        chk_left_limit = max(0, col-2)
        chk_right_limit = min(self.edge-3, col) # inclusive   
        
        # loop through the starting position of the three consecutive elements
        for cl in range(chk_left_limit, chk_right_limit + 1):
            if temp[row, cl] == temp[row, cl + 1 ] == temp[row, cl + 2 ]:
                print(row,cl)
                print("Three consecutive fail - Row")
                return False

        ### Col condition: no three same numbers next to each other allowed
        chk_up_limit = max(0, row-2)
        chk_low_limit = min(self.edge-3, row) # inclusive   
        
        # loop through the starting position of the three consecutive elements
        for rw in range(chk_up_limit, chk_low_limit + 1):
            if temp[rw, col] == temp[rw + 1, col ] == temp[rw + 2, col ]:
                print(rw,col)
                print("Three consecutive fail - Col")
                return False        
            
        ###########################
        #### Rule 2: Each row and column must have the same number of 0s and 1s
        ###########################
            
        ### Number of elements check - column
        # only need to check if the submitted number is valid. no need to care about the other number
        elem_cnt_col = (temp[:, col] == num).sum()
        if elem_cnt_col > cnt_lmt:
            print("Number of Elements Fail - Column")
            return False

        elem_cnt_row = (temp[row, :] == num).sum()
        if elem_cnt_row > cnt_lmt:
            print("Number of Elements Fail - Row")
            return False
            
        ###########################
        #### Rule 3: No identical rows or columns. This only applies when a column or row is complete.
        ###########################    
        ### Repeating column check
        crow = board[row,:]
        ccol = board[:, col]
        for r in range(self.edge):
            if r != row:
                if self.compare(crow, board[r,:]) == True:
                    print(" Repeating Row")
                    return False
        
        for c in range(self.edge):
            if c != col:
                if self.compare(ccol, board[:,c]) == True:
                    print(" Repeating Col")
                    return False
                
        ### if passes all the checks then valid
        return True
                  
         
    
    
    #### Check the next open position on the board row by row. Also very importantly, return True when the game is over, i.e. no more open positions.
    def next_open(self):

        for row in range(self.edge):
            for col in range(self.edge):
                if self.board[row, col] not in [0,1]:
                    return (row, col)
        return True
    
    
    
    
    ### The main part of the code: depth first search (DFS)
    ### recursive    
    def solve(self):
        ###
        ### end condition
        if self.next_open() == True:
            return True
        else:
            ### next position 
            row, col = self.next_open()
        
        for num in range(2):
            ### update board
            self.board[row, col] = num
            
            ### Check if the updated board satisfy the rules
            if self.valid((row, col), num) == True:
                ### recursively solve the current updated board
                ### if the current guess is valid, then return True. This will happen when we reach the end of the board.
                if self.solve() == True:
                    return True
        ### after going through all the guesses and not going into the next level, meaning the current board does not have any valid solution.
        ### reset the board and return False. return back to the previous level.
        self.board[row, col] = 9
        
        return False
    
    
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
pos = (0,0)
num = 0

b = alolboard(board)
b.solve()
b.board