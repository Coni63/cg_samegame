import random
import tqdm

from game import GameManager, BoardState, Region


class Agent:
    def __init__(self, initial_state: BoardState):
        self.G = {}
        self.initial_state = initial_state
        self.initial_state.compute_all_regions()

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
    
    def run(self, n=100):
        best_actions = None
        best_score = 0

        for _ in tqdm.tqdm(range(n)):
            actions = []
            state = self.initial_state.clone()

            # every game select a random tabuColor (can be changed to most common color with self.get_tabu_color)
            tabu = random.randint(0, 4)  # self.get_tabu_color()
            while True:
                if len(state.regions) > 0:

                    # check if we can only expand non tabu colors
                    tabu_regions = []
                    for region in state.regions:
                        if region.color != tabu:
                            tabu_regions.append(region)

                    if len(tabu_regions) > 0:
                        selected_region: Region = random.choice(tabu_regions)
                    else:
                        selected_region: Region = random.choice(state.regions)

                    row, col = selected_region.get_random_pos()
                    actions.append(f"{row} {col}")
                    state = GameManager.play(state, selected_region)
                else:
                    if state.score > best_score:
                        best_score = state.score
                        best_actions = actions
                    break

        return (best_score, best_actions)
