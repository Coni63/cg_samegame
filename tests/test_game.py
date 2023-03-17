import unittest

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
        target_hash = "10af904b32c375050e6d4495fcdf61f46f795098"

        # check same instances but different pointers
        shallow_copy = state
        self.assertEqual(id(shallow_copy), id(state))
        self.assertEqual(id(shallow_copy.board), id(state.board))

        # check different instances
        deep_clone = state.clone()
        self.assertNotEqual(id(deep_clone), id(state))
        self.assertNotEqual(id(deep_clone.board), id(state.board))

        self.assertEqual(deep_clone.get_hash(), state.get_hash())
        self.assertEqual(deep_clone.get_hash(), target_hash)

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
