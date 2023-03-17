import random

from game import GameManager, BoardState, Region


class Agent:
    def __init__(self, initial_state: BoardState):
        self.G = {}
        self.initial_state = initial_state
        self.initial_state.compute_all_regions()

    def run(self, n=100):
        best_actions = None
        best_score = 0
        for _ in range(n):
            actions = []
            state = self.initial_state.clone()
            while True:
                if len(state.regions) > 0:
                    selected_region: Region = random.choice(state.regions)
                    row, col = selected_region.get_random_pos()
                    actions.append(f"{row} {col}")
                    state = GameManager.play(state, selected_region)
                else:
                    if state.score > best_score:
                        best_score = state.score
                        best_actions = ";".join(actions)
                    break

        return (best_score, best_actions)
