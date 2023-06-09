import unittest
import glob

from game import GameManager


class TestGame(unittest.TestCase):
    def test_init(self):
        testcase = "testcases/test18.json"
        state, _ = GameManager.from_testcase(testcase)

        self.assertTupleEqual(state.board.shape, (15, 15))
        self.assertEqual(state.score, 0)

    def test_counter(self):
        testcase = "testcases/test18.json"
        state, _ = GameManager.from_testcase(testcase)

        self.assertTupleEqual(tuple(state.counter), (39, 55, 41, 56, 34))

    def test_clone(self):
        testcase = "testcases/test18.json"
        state, _ = GameManager.from_testcase(testcase)
        target_hash = 1130581700040491337

        # check same instances but different pointers
        shallow_copy = state
        self.assertEqual(id(shallow_copy), id(state))
        self.assertEqual(id(shallow_copy.board), id(state.board))

        # check different instances
        deep_clone = state.clone()
        self.assertNotEqual(id(deep_clone), id(state))
        self.assertNotEqual(id(deep_clone.board), id(state.board))

        self.assertEqual(hash(deep_clone), hash(state))
        self.assertEqual(hash(deep_clone), target_hash)

    def test_regions(self):
        testcase = "testcases/test20.json"
        state, _ = GameManager.from_testcase(testcase)
        state.compute_all_regions()

        total_group = sum(len(x) for x in state.regions)
        largest_group = max(len(x) for x in state.regions)
        self.assertEqual(len(state.regions), 45)
        self.assertEqual(total_group, 126)
        self.assertEqual(largest_group, 6)

    def test_gravity(self):
        testcase = "testcases/test1.json"
        state, _ = GameManager.from_testcase(testcase)
        state.compute_all_regions()

        self.assertEqual(len(state.regions), 12)

        new_state = GameManager.play(state, state.regions[6])
        self.assertNotEqual(id(new_state), id(state))

        new_state.compute_all_regions()
        self.assertEqual(new_state.score, 784)
        self.assertEqual(len(new_state.regions), 10)

        first_col = list(new_state.board[:, 0].flatten())
        target_col = [1, 0, 1, 1, 2, 0, 2, 2, 2, 0, 3, 1, 4, -1, -1]
        self.assertListEqual(first_col, target_col)

    def test_shift_columns(self):
        testcase = "testcases/test2.json"
        state, _ = GameManager.from_testcase(testcase)
        state.compute_all_regions()

        self.assertEqual(len(state.regions), 10)

        new_state = GameManager.play(state, state.regions[5])
        self.assertNotEqual(id(new_state), id(state))

        new_state.compute_all_regions()

        self.assertEqual(new_state.score, 784)
        self.assertEqual(len(new_state.regions), 8)

        first_row = list(new_state.board[0].flatten())
        target_row = [1, 2, 2, 0, 0, 1, 1, 4, 4, 1, 1, 2, 0, -1, -1]
        self.assertListEqual(first_row, target_row)

    def test_collisions(self):
        all_hashs = {}
        collision = False
        files = glob.glob("testcases/test*.json")
        for file in files:
            initial_state, is_validator = GameManager.from_testcase(file)
            code = hash(initial_state)
            print(file, code)
            if code not in all_hashs:
                all_hashs[code] = file
            else:
                print(f"{file} collides with {all_hashs[code]} : {code}")
                collision = True
                # break

        self.assertFalse(collision, msg="The hash function does not provide a unique hash for every tests cases")

