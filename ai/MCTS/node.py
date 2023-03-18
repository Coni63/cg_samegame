from __future__ import annotations
import math
from typing import Tuple
from game import GameManager, BoardState, Region
import random


class Node:
    state: BoardState
    parent: Node
    action_taken: Tuple[int, int]
    children: list[Node]
    visited: int
    sum_score: int
    terminal: bool

    def __init__(self, state: BoardState, parent: Node, action_taken: Tuple[int, int]):
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.children = []
        self.visited = 0
        self.sum_score = 0
        self.terminal = len(state.regions) == 0

    def select_child(self, exploration_constant=1.4):
        if len(self.children) == 0:
            return None

        best_score = 0
        best_child = None
        for child in self.children:
            # new nodes are explored at least once
            if child.visited == 0:
                return child
            score = (
                math.log(child.sum_score / child.visited) +
                exploration_constant * math.sqrt(math.log(self.visited) / child.visited)
            )  # UCB1
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def expand(self):
        for region in self.state.regions:
            action_taken = region.get_random_pos()
            child_state = GameManager.play(self.state, region)
            child_node = Node(child_state, parent=self, action_taken=action_taken)
            self.children.append(child_node)

    def simulate(self):
        state = self.state.clone()
        while True:
            if len(state.regions) > 0:
                selected_region: Region = random.choice(state.regions)
                state = GameManager.play(state, selected_region)
            else:
                break
        return state.score

    def backpropagate(self, score):
        node = self
        while node is not None:
            node.visited += 1
            node.sum_score += score
            node = node.parent
