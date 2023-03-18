import random

from game import GameManager, BoardState

"""
Do not use - too slow and too expensive in memory
Due to high branching factor
"""


class Agent:
    def __init__(self, initial_state: BoardState):
        self.initial_state = initial_state

    def get_tabu_color(self):
        highest_count = 0
        idx = []
        for i, c in enumerate(self.initial_state.counter):
            if c == highest_count:
                idx.append(i)
            elif c > highest_count:
                highest_count = c
                idx = [i]

        return random.choice(idx)

    def run(self):
        tabu = self.get_tabu_color()
        print(f"TabuColor: {tabu} - {self.initial_state.counter}")

        Q = [([], self.initial_state)]
        visited = set()
        best_actions = None
        best_score = 0
        while len(Q) > 0:
            actions, state = Q.pop(0)

            # check if we can only expand non tabu colors
            can_tabu = False
            for region in state.regions:
                can_tabu |= region.color != tabu

            for region in state.regions:
                # if we can skip the tabu color, we don't expand those nodes
                if can_tabu and region.color == tabu:
                    continue

                row, col = region.get_random_pos()
                new_actions = actions[:] + [f"{row} {col}"]
                new_state = GameManager.play(state, region)

                if new_state in visited:
                    # print("skipped")
                    continue

                visited.add(new_state)

                if len(new_state.regions) > 0:
                    Q.append((new_actions, new_state))
                elif new_state.score > best_score:
                    best_score = new_state.score
                    best_actions = new_actions

        return (best_score, best_actions)