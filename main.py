import glob
from hashlib import sha1
import numpy as np
import json
from ai.random_search import Agent
from game import GameManager

def get_hash(arr: np.array):
    return sha1(arr).hexdigest()



if __name__ == "__main__":
    ans = {}
    total_score = 0
    files = glob.glob("testcases/test*.json")
    for file in files:
        initial_state = GameManager.from_testcase(file)
        code = get_hash(initial_state.board)
        agent = Agent(initial_state)
        best_score, best_action = agent.run(1)
        total_score += best_score
        ans[code] = best_action
    print(total_score)
    with open("output.txt", "w") as f:
        json.dump(ans, f)