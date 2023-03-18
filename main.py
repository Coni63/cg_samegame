import glob
import json
# from ai.random_search import Agent
# from ai.BFS import Agent
# from ai.MCTS import Agent
# from ai.tabuBFS import Agent
from ai.tabu_random_search import Agent
from ai.utils import Saver
from game import GameManager


def train(files: list[str]):
    saver = Saver("output.db")
    total_score = 0

    for file in files:
        print(file)
        initial_state, is_validator = GameManager.from_testcase(file)
        agent = Agent(initial_state)
        best_score, best_action = agent.run(15000)  # for the random search
        # best_score, best_action = agent.run()  # for the BFS
        # best_score, best_action = agent.run(n_iter=2000, n_rollout=10)
        action_str = ";".join(best_action)
        total_score += best_score

        saver.save(testfile=file, actions=action_str, score=best_score)


def eval(files: list[str], only_validator=True):
    saver = Saver("output.db")
    total = 0
    for file in files:
        initial_state, is_validator = GameManager.from_testcase(file)
        if only_validator and not is_validator:
            continue

        try:
            actions, score = saver.get_best(file[10:])
        except:
            continue

        total += score
        print(file, score)

    print("total", total)


def make_dictionary(files: list[str]):
    saver = Saver("output.db")
    ans = {}

    for file in files:
        initial_state, is_validator = GameManager.from_testcase(file)
        try:
            actions, score = saver.get_best(file[10:])
        except:
            continue
        code = hash(initial_state)
        ans[code] = actions

    with open("output.txt", "w") as f:
        json.dump(ans, f)


def remove_duplicates():
    file_to_hash = {}
    hash_to_hash = {}
    titles = {}

    for file in glob.glob("testcases/test*.json"):
        initial_state, is_validator = GameManager.from_testcase(file)
        code = str(hash(initial_state))

        with open(file, "r") as f:
            data = json.load(f)

        name = data["title"]["2"].replace(" (recolored)", "")

        if name in titles:
            hash_to_hash[code] = file_to_hash[titles[name]]
        else:
            hash_to_hash[code] = code

    return hash_to_hash


def list_files_to_process():
    ans = []
    for file in glob.glob("testcases/test*.json"):
        with open(file, "r") as f:
            data = json.load(f)

        name = data["title"]["2"]

        # the 5 custom ones are already solved (test[1-5].json)
        if not name.startswith("Standard"):
            continue

        # not required
        if name.endswith("(recolored)"):
            continue

        ans.append(file)
    print(ans)


if __name__ == "__main__":
    # list_files_to_process()
    # print(remove_duplicates())
    # files = glob.glob("testcases/test*.json")

    files = [
        'testcases\\test10.json',
        # 'testcases\\test12.json',
        # 'testcases\\test13.json',
        # 'testcases\\test14.json',
        # 'testcases\\test16.json',
        # 'testcases\\test17.json',
        # 'testcases\\test18.json',
        # 'testcases\\test19.json',
        # 'testcases\\test21.json',
        # 'testcases\\test22.json',
        # 'testcases\\test23.json',
        # 'testcases\\test24.json',
        # 'testcases\\test26.json',
        # 'testcases\\test27.json',
        # 'testcases\\test28.json',
        # 'testcases\\test29.json',
        # 'testcases\\test6.json',
        # 'testcases\\test7.json',
        # 'testcases\\test8.json',
        # 'testcases\\test9.json'
    ]

    train(files)
    # eval(files, only_validator=False)
    # make_dictionary(files)
