from typing import Set, Tuple
import json
import numpy as np

from .board import BoardState


class GameManager:

    @staticmethod
    def from_testcase(testcase: str) -> Tuple[BoardState, bool]:
        with open(testcase, "r") as f:
            data = json.load(f)

        rows = data["testIn"].split("\n")
        grid = [[int(value) for value in row.strip().split(" ")] for row in rows[::-1]]  # flip as the grip has a 0 on the bottom

        return BoardState(np.array(grid, dtype=np.int8), score=0), data["isValidator"] == "true"

    @staticmethod
    def play(state: BoardState, region: Set) -> BoardState:
        left = 14
        right = 0
        top = 14
        color = -1

        new_state = state.clone()

        for r, c in region:
            color = new_state.board[r, c]
            new_state.board[r][c] = -1
            # get the bounding box to update only this part
            left = min(left, c)
            right = max(right, c)
            top = min(top, r)

        new_state.score += (len(region)-2)*(len(region)-2)

        new_state.counter[color] -= len(region)

        GameManager._apply_gravity(new_state, left, right, top)
        GameManager._shift_column(new_state, left)

        if new_state.board[0, 0] == -1:  # grid is Y-inverted so this is bottom left
            new_state.score += 1000
            new_state.regions = []
            return new_state

        new_state.compute_all_regions()
        return new_state

    @staticmethod
    def _apply_gravity(state: BoardState, min_col: int, max_col: int, top: int) -> None:
        # attention the board is reversed, the top is 0 and the bottom is 14
        for col in range(min_col, max_col+1):
            offset = 0
            for row in range(top, 15):
                if state.board[row, col] == -1:
                    offset += 1
                    continue

                if offset > 0:
                    state.board[row-offset, col] = state.board[row, col]
                    state.board[row, col] = -1

    @staticmethod
    def _shift_column(state: BoardState, left: int) -> None:
        offset = 0
        for i in range(left, 15):
            if state.board[0, i] == -1:
                offset += 1
                continue

            if offset == 0:
                continue

            state.board[:, i-offset] = state.board[:, i]
            state.board[:, i] = -1
