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

    slide_iter(board)


def slide_iter(board):
    w, h = board.shape
    space = np.array(np.where(board == 0)).T[0]
    print(space)
    print(board[tuple(space)])
    print(DIRECTIONS)
    adjacencies = space + DIRECTIONS
    print("adj", adjacencies)
    in_bounds = np.logical_and.reduce(
        [
            adjacencies[:, 0] >= 0,
            adjacencies[:, 0] < w,
            adjacencies[:, 1] >= 0,
            adjacencies[:, 1] < h,
        ]
    )
    print("in_bounds", in_bounds)
    adjacencies = adjacencies[in_bounds]
    print("adj", adjacencies)
    # adjacent_tiles = board[adjacencies[..., 0], adjacencies[..., 1]]
    # print("tiles", adjacent_tiles)
    print("perm", permute(board, (0, 0), (0, 1)))


def permute(board, pt_1, pt_2):
    pt_1, pt_2 = tuple(pt_1), tuple(pt_2)
    board_2 = np.array(board)
    # print(board, id(board))
    # print(board_2, id(board_2))
    # print(pt_1, pt_2)
    board_2[pt_1] = board[pt_2]
    board_2[pt_2] = board[pt_1]
    return board_2


if __name__ == "__main__":
    main()
