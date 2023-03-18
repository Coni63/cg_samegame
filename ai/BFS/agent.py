from game import GameManager, BoardState

"""
Do not use - too slow and too expensive in memory
Due to high branching factor
"""


class Agent:
    def __init__(self, initial_state: BoardState):
        self.initial_state = initial_state
        self.initial_state.compute_all_regions()
        self.Q = [([], self.initial_state)]

    def run(self):
        visited = set()
        best_actions = None
        best_score = 0
        while len(self.Q) > 0:
            actions, state = self.Q.pop(0)
            print("depth:", len(actions))
            for region in state.regions:
                row, col = region.get_random_pos()
                new_actions = actions[:] + [f"{row} {col}"]
                new_state = GameManager.play(state, region)

                if new_state in visited:
                    # print("skipped")
                    continue

                visited.add(new_state)

                if len(new_state.regions) > 0:
                    self.Q.append((new_actions, new_state))
                elif new_state.score > best_score:
                    best_score = new_state.score
                    best_actions = new_actions

        return (best_score, best_actions)
