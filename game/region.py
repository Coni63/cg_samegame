from typing import Tuple, Set
import random


class Region:
    def __init__(self, pos, color):
        self.pos: Set[Tuple[int, int]] = pos
        self.color = color

    def get_random_pos(self) -> Tuple[int, int]:
        return random.sample(self.pos, 1)[0]

    def __iter__(self) -> Tuple[int, int]:
        for row, col in self.pos:
            yield row, col

    def __len__(self) -> int:
        return len(self.pos)
