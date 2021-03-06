import unittest
import random
import time

from short_fns import GameOfLife

class TestGameOfLife(unittest.TestCase):

    def test_init(self):
        try:
            mygame = GameOfLife(rows=0, cols=0)
            raise AssertionError("Must have both rows and cols!")
        except AssertionError:
            pass
        mygame = GameOfLife(rows=2, cols=2)

    def test_zero_out(self):
        mygame = GameOfLife(rows=2, cols=2)
        mygame.zero_out()
        self.assertEqual(mygame.live_cell_count(), 0)
        mygame.seed(2)
        self.assertNotEqual(mygame.live_cell_count(), 0)
        mygame.zero_out()
        self.assertEqual(mygame.live_cell_count(), 0)

    def test_birth(self):
        # if you have 3 neighbors and are dead then you get birthed
        mygame = GameOfLife(rows=2, cols=2)
        mygame.seed(3)
        self.assertEqual(mygame.live_cell_count(), 3)
        changed = mygame.advance()
        self.assertEqual(changed, True)
        self.assertEqual(mygame.live_cell_count(), 4)

    def test_death(self):
        mygame = GameOfLife(rows=3, cols=3)
        while mygame.live_cell_count() != 9:
            random.seed(time.time())
            mygame.seed(9)

        changed = mygame.advance()
        self.assertEqual(changed, True)
        self.assertEqual(mygame.live_cell_count(), 4)

        changed = mygame.advance()
        self.assertEqual(changed, True)
        self.assertEqual(mygame.live_cell_count(), 0)

        changed = mygame.advance()
        self.assertEqual(changed, False)


    def test_steady_state_condition(self):
        mygame = GameOfLife(rows=2, cols=2)
        while mygame.live_cell_count() != 4:
            random.seed(time.time())
            mygame.seed(4)
        changed = mygame.advance()
        self.assertEqual(changed, False)


if __name__ == '__main__':
    unittest.main()
