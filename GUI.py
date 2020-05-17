# GUI.py
import pygame
from solver import alolboard
import time
### need to call this to initiate
pygame.init()
pygame.font.init()


# display is a module, and set_mode is a function inside that module. It actually creates an instance of the pygame.Surface class, and returns that. 


class GUI:
    """
    This class plot the skeloton of the board. 
    The Grid contains Cubes which contains values and is responsible for putting numbers on the board.
    
    
    Overall Logic:
        1. Maintain the board data: self.board
        2. Maintain the visual board: self.win
        3. Make sure that the data and teh visualization are synced.
    """
    
    def __init__(self, board, grid_length, answer):
        """
        This class defines the visualization of the board using pygame. 
        The Grid contains cubes which has temporary and placed numbers in it.
        
        board: a numpy array of the board
        answer: a numpy array of the board answers. the final board.
        grid_length: the width of the grid, grid is a square
  
        """
        
        ## the current state of the board
        self.board = board.copy()
        
        ## initial board: which specifies which numbers cannot be changed.
        self.init_board = board.copy()
        
        ## final board
        self.answer = answer.copy()
        
        ## The parameters for the grid
        self.grid_length = int(grid_length)
        
        ## number of elements in one row/column
        self.n_elems = len(board)
        
        ## unit length
        self.unit_length = int(grid_length / len(board))
        
        ## the window used in the pygame. the visualization piece. Initialized to be None
        self.win = None
        
        ## the selected cell. (row, col)
        self.selected = None
        
        ## define the spec of buttons
        self.submit_button_xy = (1/2* self.unit_length, self.grid_length + 1/4 * self.unit_length)
        
        self.restart_button_xy = (2.5 * self.unit_length, self.grid_length + 1/4 * self.unit_length)
        
        self.text_xy = (1/2* self.unit_length, self.grid_length + 5/4 * self.unit_length)
        
        self.button_wh = (self.unit_length,  self.unit_length/2)
        
        ## see if the board is fully filled
        self.filled = None
        
        ## the text displaying on the board
        self.text = None
    
    def show_grid(self):
        """
        The window with initial values. will be used to refresh each frame
        """
        ## initilize the window, leave some room on the height edge to show timer
        self.win = pygame.display.set_mode((self.grid_length, self.grid_length + 2*self.unit_length))
        ## white background
        self.win.fill((255, 255, 255))
        
        ######################
        ## draw the grid lines
        ## line(surface, color, start_pos, end_pos, width); pos is the (x,y) tuple. x is the width, y is the height.
        for r in range(self.n_elems + 1):                
            pygame.draw.line(self.win, (0,0,0), (0, r * self.unit_length), (self.grid_length , r * self.unit_length), 2)
        
        for c in range(self.n_elems):
            pygame.draw.line(self.win, (0,0,0), (c * self.unit_length, 0), (c * self.unit_length, self.grid_length), 2)    
            
        ######################
        ## font for the button
        fnt = pygame.font.SysFont("comicsans", int(self.unit_length*1/2/3*2))
        
        ######################
        ## construct the submit button
        ## x, y are the top left corner coordinate, width, length
        x, y = self.submit_button_xy 
        w, h = self.button_wh
        pygame.draw.rect(self.win, (0,0,0), (x, y, w, h), 2)   
        ## cannot submit if there is still unfilled numbers
        if self.filled == False:
            text = fnt.render("submit", 1, (192,192,192))
        else:
            text = fnt.render("submit", 1, (0,0,0))            
        self.win.blit(text, (x + w *0.5 - text.get_width()/2, y+ h *0.5 - text.get_height()/2))
        ######################
        ## construct the restart button        
        x, y = self.restart_button_xy 
        w, h = self.button_wh
        pygame.draw.rect(self.win, (0,0,0), (x, y, w, h), 2)     
        text = fnt.render("restart", 1, (0,0,0))
        self.win.blit(text, (x + w *0.5 - text.get_width()/2, y+ h *0.5 - text.get_height()/2))                   
            
    def click_cell(self, pos):
        """
        This function is only triggered when there is click of the mouse. if click anywhere that is not on the board, any selected cell will be de-selected.
        pos: (width, height), where the mouse is clicking on the board
        when clicked, the default selected cell would be None. unless we are clicking the right spot.
        """
        self.selected = None 
        self.text = None
        
        if pos[0] < self.grid_length and pos[1] < self.grid_length:
            x = pos[0] // self.unit_length
            y = pos[1] // self.unit_length
            ### row, cell
            ### important logic, do not allow for selection of given cells!!!!
            if self.init_board[int(y), int(x)] == 9:
                self.selected = (int(y),int(x))
        ## when clicking the submit button
        elif pos[0]>self.submit_button_xy[0] and pos[0]<self.submit_button_xy[0] + self.button_wh[0] and  pos[1]>self.submit_button_xy[1] and pos[1]<self.submit_button_xy[1] + self.button_wh[1]:
            ## only works when you filled all the empty cells
            fnt = pygame.font.SysFont("comicsans", int(self.unit_length*1/2/3*2))

            
            if self.filled == True:
                if (self.board == self.answer).all():
                    self.text = fnt.render("Congrat", 1, (0,0,0))
                else:
                    self.text = fnt.render("Wrong answer", 1, (0,0,0))
            else:
                self.text = fnt.render("Incomplete", 1, (0,0,0))
                
                    
        ## when clicking the restart button
        elif pos[0]>self.restart_button_xy[0] and pos[0]<self.restart_button_xy[0] + self.button_wh[0] and  pos[1]>self.restart_button_xy[1] and pos[1]<self.restart_button_xy[1] + self.button_wh[1]:
            ### restart the board
            self.board = self.init_board.copy()
            ## the selected cell. (row, col)
            self.selected = None
                
            
                      

    def update_cell(self, number):
        """
        number: the number user input into the board
        0, 1 or 9. 9 corresponds to delete
        """
        self.board[self.selected[0], self.selected[1]] = number
            
    def refresh_win(self):
        """
        The function is used to refresh the winow
        
        starts with re-plot the initial board
        
        
        """
        ### refresh the grid to see if the board is done
        self.filled = 9 not in self.board
        
        self.show_grid()
        
        ### then draw the selected window if within the bound
        if self.selected != None:
            ### self.selected is r and c
            x = self.selected[1] * self.unit_length
            y = self.selected[0] * self.unit_length            
            pygame.draw.rect(self.win, (255,0,0), (x, y, self.unit_length,  self.unit_length), 2)
        
        ### then draw the numbers on board
        fnt = pygame.font.SysFont("comicsans", int(self.unit_length/4*3))
        for r in range(self.n_elems):
            for c in range(self.n_elems):
                
                ### Check the current board if it is empty
                if self.board[r,c] != 9:         
                    ### if the number is in the initial board, black
                    if self.init_board[r,c] != 9:
                        text = fnt.render(str(self.init_board[r,c]), 1, (0,0,0))
                    ### blue
                    else:
                        text = fnt.render(str(self.board[r,c]), 1, (0,128,250))                        
                    ### make sure we are at the number are at the center of the box
                    ### win.blit(source, position (width, height))
                    self.win.blit(text, (c * self.unit_length + self.unit_length *0.5 - text.get_width()/2, r * self.unit_length + self.unit_length *0.5 - text.get_height()/2))
                                          
        ### display text
        if self.text != None:

            self.win.blit(self.text,self.text_xy )    
            
            




def run_game(grid):
    pygame.display.set_caption("ALOL Game")
    running = True
    while running:
        """
        while loop for frame refreshing
        it is important to know that there could be multiple actions between two frames happen.
        This is the key to understand the while loop and event loop.
        events need to be cleared out each time as well.
        
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ### cell selection
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                grid.click_cell(pos)
            
                
            ### update cell, if enterned anything other than the 0, 1 or delete, do not update 
            if grid.selected != None:
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_KP1]:
                        key = 1
                        grid.update_cell(key)
                    elif event.key in [pygame.K_0, pygame.K_KP0]:
                        key = 0
                        grid.update_cell(key)
                    elif event.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
                        key = 9
                        grid.update_cell(key)
                    
        ### refresh the board after each frame
        grid.refresh_win()
        win = grid.win
                   
        pygame.display.update()
        # pygame.display.flip()
    
    pygame.quit()



from solver import alolboard
import numpy as np
board_1 = np.array([[9, 0, 9, 9, 9, 1, 9, 9],
                   [0, 1, 9, 0, 9, 9, 1, 9],
                   [9, 9, 0, 0, 9, 9, 0, 9],
                   [9, 9, 9, 9, 9, 0, 9, 9],
                   [9, 9, 9, 0, 9, 9, 1, 9],
                   [9, 9, 1, 9, 9, 9, 9, 0],
                   [1, 9, 9, 1, 9, 9, 9, 9],
                   [1, 9, 9, 9, 9, 9, 9, 1]])

bd1 = alolboard(board_1)
bd1.solve()

print(bd1.board)
grid_length = 600
       
grid1 = GUI(board_1, grid_length, bd1.board)
run_game(grid1)










