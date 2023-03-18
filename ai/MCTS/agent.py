import random
import tqdm
from game import BoardState  # GameManager,  Region
from .node import Node


class Agent:
    def __init__(self, initial_state: BoardState):
        self.root = Node(initial_state, None, None)

    def run(self, n_iter=100, n_rollout=100):
        for i in tqdm.tqdm(range(n_iter)):
            node = self.root
            # Selection
            while len(node.children) > 0:
                node = node.select_child()
            # Expansion
            if not node.terminal:
                node.expand()  # node.state.get_actions())
                child_node = random.choice(node.children)
            else:
                child_node = node

            for i in range(n_rollout):  # run 10 rollout to have better approximation
                # Simulation
                score = child_node.simulate()
                # Backpropagation
                child_node.backpropagate(score)

        # construct best path
        all_actions = []
        node = self.root
        while len(node.children) > 0:
            node = node.select_child(exploration_constant=0)
            all_actions.append(node.action_taken)
        return node.sum_score // node.visited, [f"{row} {col}" for row, col in all_actions]
