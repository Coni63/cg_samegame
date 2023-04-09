import glob
import json
from ai.utils import Saver
from game.game import GameManager

files = [
        'testcases\\test10.json',
        'testcases\\test12.json',
        'testcases\\test13.json',
        'testcases\\test14.json',
        'testcases\\test16.json',
        'testcases\\test17.json',
        'testcases\\test18.json',
        'testcases\\test19.json',
        'testcases\\test21.json',
        'testcases\\test22.json',
        'testcases\\test23.json',
        'testcases\\test24.json',
        'testcases\\test26.json',
        'testcases\\test27.json',
        'testcases\\test28.json',
        'testcases\\test29.json',
        'testcases\\test6.json',
        'testcases\\test7.json',
        'testcases\\test8.json',
        'testcases\\test9.json'
]

total = 0
ans = {}
for file in files:
    initial_state, is_validator = GameManager.from_testcase(file)    
    code = hash(initial_state)

    best_action = ""
    best_score = 0

    for save in glob.glob("output*.db"):
        saver = Saver(save)
        record = saver.get_best(file[10:])
        if record is None:
            continue

        actions, score = record
        if score > best_score:
            best_score = score
            best_action = actions
    total += best_score
    ans[code] = best_action

print(total * 2)
with open("output.txt", "w") as f:
    json.dump(ans, f)