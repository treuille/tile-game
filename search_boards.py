import numpy as np
import sys
import math
from out_of_core import IntSet

DIRECTIONS = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])


def main():
    # Parse the number of tiles
    w, h = map(int, sys.argv[1:])
    tiles = w * h
    max_solutions = math.factorial(tiles)

    # Show header information.
    print(f"Testing tiles with size {w}x{h}...")
    print(f"At most, it can have {max_solutions} solutions.")

    return

    # Create the initial board
    board = np.arange(tiles, dtype="B").reshape(w, h)

    # # Find the solution recursively.
    # all_boards_1 = find_all_boards_recursively(board)
    # print(f"Found {len(all_boards_1)} / {max_solutions} boards recursively.")
    # print(f"The solution ID is {hash(tuple(sorted(all_boards_1)))}.")

    # Find the solution iteratively.
    all_boards_2 = find_all_boards_iteratively(board)
    print(f"Found {len(all_boards_2)} / {max_solutions} boards iteratively.")
    # print(f"The solution ID is {hash(tuple(sorted(all_boards_2)))}.")


def find_all_boards_recursively(board: np.ndarray) -> set:
    all_boards = set()
    recurse_through_all_boards(board, all_boards)
    return all_boards


def find_all_boards_iteratively(board: np.ndarray) -> set:

    all_boards = IntSet()
    all_boards.add(get_board_key(board))
    unprocessed_boards = [board]
    while unprocessed_boards:
        board = unprocessed_boards.pop()
        board_key = get_board_key(board)
        assert board_key in all_boards
        for board in slide_iter(board):
            board_key = get_board_key(board)
            if board_key not in all_boards:
                unprocessed_boards.append(board)
                all_boards.add(board_key)
                if len(all_boards) % 100000 == 0:
                    print(
                        f"There are now {len(unprocessed_boards)} boards to process, "
                        f"and {len(all_boards)} discovered boards."
                    )
    return all_boards


def get_board_key(board: np.ndarray) -> int:
    """Returns an immutable key fot the board which can be placed in a set."""
    return hash(board.tobytes())


def recurse_through_all_boards(board: np.ndarray, all_boards: set):
    """Depth-first search through all adjacent boards."""
    board_key = get_board_key(board)
    if board_key in all_boards:
        return
    assert board_key not in all_boards
    all_boards.add(board_key)
    for permuted_board in slide_iter(board):
        recurse_through_all_boards(permuted_board, all_boards)


def slide_iter(board):
    w, h = board.shape
    space = np.array(np.where(board == 0)).T[0]
    adjacencies = space + DIRECTIONS
    in_bounds = np.logical_and.reduce(
        [  # type: ignore
            adjacencies[:, 0] >= 0,
            adjacencies[:, 0] < w,
            adjacencies[:, 1] >= 0,
            adjacencies[:, 1] < h,
        ]
    )
    adjacencies = adjacencies[in_bounds]
    return (permute(board, space, adj) for adj in adjacencies)


def permute(board, pt_1, pt_2):
    pt_1, pt_2 = tuple(pt_1), tuple(pt_2)
    board_2 = np.array(board)
    board_2[pt_1] = board[pt_2]
    board_2[pt_2] = board[pt_1]
    return board_2


if __name__ == "__main__":
    main()
