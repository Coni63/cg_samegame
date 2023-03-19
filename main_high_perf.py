from __future__ import annotations
from typing import Set, Tuple
from queue import Queue
import random
import json
import numpy as np
import tqdm


class Board:

    def __init__(self, values: list[list[int]], score=0):
        self.board = values
        self.score = score

    def reset(self, ref: Board):
        self.board = np.array(ref.board)
        self.score = ref.score

    def clone(self):
        return Board(np.array(self.board), self.score)

    def get_random_region(self, tabuColor=None) -> Set[Tuple[int, int]]:
        offset = np.array([16, 1])
        all_tabu = (np.argwhere(self.board == tabuColor) @ offset).tolist()
        all_non_tabu = (np.argwhere((self.board > -1) & (self.board != tabuColor)) @ offset).tolist()

        random.shuffle(all_non_tabu)
        for pos in all_non_tabu:
            region = self._compute_regions(pos)
            if len(region) > 1:
                return region

        random.shuffle(all_tabu)
        for pos in all_tabu:
            region = self._compute_regions(pos)
            if len(region) > 1:
                return region

        return None

    def play(self, region: Set[int]) -> bool:
        left = 14
        right = 0
        top = 14

        for pos in region:
            r, c = pos >> 4, pos & 15
            self.board[r, c] = -1
            # get the bounding box to update only this part
            left = min(left, c)
            right = max(right, c)
            top = min(top, r)

        self.score += (len(region)-2)*(len(region)-2)

        self._apply_gravity(left, right, top)
        self._shift_column(left)

        if self.board[0, 0] == -1:  # grid is Y-inverted so this is bottom left
            self.score += 1000
            return True

        return False

    def _apply_gravity(self, min_col: int, max_col: int, top: int) -> None:
        # attention the board is reversed, the top is 0 and the bottom is 14
        for col in range(min_col, max_col+1):
            offset = 0
            for row in range(top, 15):
                if self.board[row, col] == -1:
                    offset += 1
                    continue

                if offset > 0:
                    self.board[row-offset, col] = self.board[row, col]
                    self.board[row, col] = -1

    def _shift_column(self, left: int) -> None:
        offset = 0
        for i in range(left, 15):
            if self.board[0, i] == -1:
                offset += 1
                continue

            if offset == 0:
                continue

            self.board[:, i-offset] = self.board[:, i]
            self.board[:, i] = -1

    def _compute_regions(self, xxyy: int) -> Set[int]:
        r, c = xxyy >> 4, xxyy & 15
        color = self.board[r, c]
        region = set()
        Q = Queue()

        Q.put(xxyy)

        while not Q.empty():
            xxyy = Q.get()
            r, c = xxyy >> 4, xxyy & 15
            if self.board[r, c] != color:
                continue

            if xxyy in region:
                continue

            region.add(xxyy)

            r << 4 | c
            if c > 0:
                Q.put(r << 4 | (c-1))
            if c < 14:
                Q.put(r << 4 | (c+1))
            if r > 0:
                Q.put((r-1) << 4 | c)
            if r < 14:
                Q.put((r+1) << 4 | c)
        return region


class Agent:
    def __init__(self, initial_state: Board):
        self.initial_state = initial_state
        self.running_state = initial_state.clone()

    def run(self, n=100):
        best_actions = None
        best_score = 0

        for _ in tqdm.tqdm(range(n)):
            self.running_state.reset(self.initial_state)
            tabu = random.randint(0, 4)

            actions = []
            while True:
                selected_region: Set[int] = self.running_state.get_random_region(tabu)
                if selected_region is None:  # no more group
                    break

                done = self.running_state.play(selected_region)
                pos = selected_region.pop()
                row, col = pos >> 4, pos & 15
                actions.append(f"{row} {col}")
                if done:
                    break

            if self.running_state.score > best_score:
                # print("New best score", self.running_state.score)
                best_score = self.running_state.score
                best_actions = actions

        return (best_score, ";".join(best_actions))


def load(testcase: str) -> np.array:
    with open(testcase, "r") as f:
        data = json.load(f)

    rows = data["testIn"].split("\n")
    grid = [[int(value) for value in row.strip().split(" ")] for row in rows[::-1]]  # flip as the grip has a 0 on the bottom

    return np.array(grid, dtype=np.int8)


if __name__ == "__main__":
    file = 'testcases\\test10.json'
    arr = load(file)
    board = Board(arr)
    agent = Agent(board)
    best_score, best_actions = agent.run(15000)
    print(best_score, best_actions)
