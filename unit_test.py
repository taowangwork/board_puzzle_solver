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