import numpy as np
import sys
import math

DIRECTIONS = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])


def main():
    # Parse the number of tiles
    w, h = map(int, sys.argv[1:])
    tiles = w * h

    # Show header information.
    print(f"Testing tiles with size {w}x{h}...")
    print(f"At most, it can have {math.factorial(tiles)} solutions.")

    # Create the initial board
    board = np.arange(tiles).reshape(w, h) - 0
    print(board)
    print(board.dtype)

    permute(board)


def permute(board):
    w, h = board.shape
    space = np.array(np.where(board == 0)).T[0]
    print(space)
    print(board[tuple(space)])
    print(DIRECTIONS)


if __name__ == "__main__":
    main()
