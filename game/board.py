from __future__ import annotations

from typing import Tuple, Set
from queue import Queue
from hashlib import sha1
import numpy as np

from .region import Region

class BoardState:

    def __init__(self, values: list[list[int]], score=0, regions=None):
        self.board = values
        # self.board.flags.writeable = False
        self.score = score
        self.counter = list(np.count_nonzero(self.board == i) for i in range(5))
        self.regions = regions

    def clone(self) -> BoardState:
        return BoardState(np.copy(self.board), self.score, self.regions)

    def get_hash(self):
        return sha1(self.board).hexdigest()

    def compute_all_regions(self):
        all_visited = set()
        self.regions = []
        for r in range(15):
            for c in range(15):
                if self.board[r, c] == -1:
                    continue

                pos = (r, c)
                if pos in all_visited:
                    continue

                region = self._compute_regions(pos)

                all_visited |= region

                if len(region) > 1:
                    # print(region)
                    self.regions.append(Region(region, self.board[r, c]))

    def _compute_regions(self, pos: Tuple[int, int]) -> Set:
        color = self.board[pos[0], pos[1]]
        region = set()
        Q = Queue()

        Q.put(pos)

        while not Q.empty():
            r, c = Q.get()

            if self.board[r, c] != color:
                continue

            if (r, c) in region:
                continue

            region.add((r, c))

            if c > 0:
                Q.put((r, c-1))
            if c < 14:
                Q.put((r, c+1))
            if r > 0:
                Q.put((r-1, c))
            if r < 14:
                Q.put((r+1, c))
        return region
