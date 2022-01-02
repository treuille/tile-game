import numpy as np
import sys
import math

DIRECTIONS = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])


def main():
    # Parse the number of tiles
    w, h = map(int, sys.argv[1:])
    tiles = w * h
    max_solutions = math.factorial(tiles)

    # Show header information.
    print(f"Testing tiles with size {w}x{h}...")
    print(f"At most, it can have {max_solutions} solutions.")

    # Create the initial board
    board = np.arange(tiles).reshape(w, h) - 0
    all_boards = set()
    # print(board)
    # print(board.dtype)
    find_all_boards(board, all_boards)
    print(f"Found {len(all_boards)} / {max_solutions} boards.")
    # x = set()
    # print(x)

    # def add_1(x):
    #     x.add(1)

    # add_1(x)
    # print(x)
    # add_1(x)
    # print(x)

    # # all_boards = set()
    # print(all_boards)
    # return
    # print(all_boards)
    # print(all_boards)

    # board = permute(board, (0, 0), (1, 1))
    # all_boards.add(tuple(board.flat))
    # print(all_boards)
    # # print("===")
    # # print(board)
    # # print("===")


def find_all_boards(board: np.ndarray, all_boards: set):
    """Depth-first search through all adjacent boards."""
    board_key = tuple(board.flat)
    if board_key in all_boards:
        return
    assert board_key not in all_boards
    all_boards.add(board_key)
    for permuted_board in slide_iter(board):
        print(f"found ({len(all_boards)} total))")
        print(permuted_board)
        find_all_boards(permuted_board, all_boards)
        # final
        # board_key = tuple(permuted_board.flat)
        # if board_key
        # print(permuted_board)
        # all_boards.add()
        # print(all_boards)
    # # # print("permuted", permuted_boards)
    # for


def slide_iter(board):
    w, h = board.shape
    space = np.array(np.where(board == 0)).T[0]
    # print(space)
    # print(board[tuple(space)])
    # print(DIRECTIONS)
    adjacencies = space + DIRECTIONS
    # print("adj", adjacencies)
    in_bounds = np.logical_and.reduce(
        [  # type: ignore
            adjacencies[:, 0] >= 0,
            adjacencies[:, 0] < w,
            adjacencies[:, 1] >= 0,
            adjacencies[:, 1] < h,
        ]
    )
    # print("in_bounds", in_bounds)
    adjacencies = adjacencies[in_bounds]
    # print("adj", adjacencies)
    # adjacent_tiles = board[adjacencies[..., 0], adjacencies[..., 1]]
    # print("tiles", adjacent_tiles, adjacent_tiles.shape)

    return (permute(board, space, adj) for adj in adjacencies)
    # print("perm", permute(board, (0, 0), (1, -1)))


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
