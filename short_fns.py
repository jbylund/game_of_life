#!/usr/bin/env python
"""
Any live cell with fewer than two live neighbours dies, as if by underpopulation.
Any live cell with two or three live neighbours lives on to the next generation.
Any live cell with more than three live neighbours dies, as if by overpopulation.
Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

So keep track of state of cell (live/dead)
and counts of neighbors (birth of cell increments all neighbors (8) by 1, death of cell decrements live neighbors by 1)
"""

import itertools
import pprint
import random
import time


class GameOfLife:
    LIVE = 1
    DEAD = 0

    def __init__(self, rows=4, cols=4):
        self.rows, self.cols = rows, cols
        self.live_cells = set()
        self.neighbors_map = self.get_neighbors_map()

    def get_neighbors_map(self):
        nm = set(itertools.product(range(-1,2), range(-1,2)))
        nm.remove((0,0))
        return nm

    def get_dense_cells(self):
        return set(itertools.product(range(self.rows), range(self.cols)))

    def zero_out(self):
        self.live_cells.clear()

    def dump(self):
        # turn it into a dense representation and dump that
        print("Cell states:")
        as_dense = [[int((rownum, colnum) in self.live_cells) for rownum in range(self.rows)] for colnum in range(self.cols)]
        pprint.pprint(sorted(as_dense), width=3*self.rows + 3)
        print(self.live_cell_count())

    def randcell(self):
        return random.randint(0, self.rows), random.randint(0, self.cols)

    def seed(self, num_cells):
        self.zero_out()
        p = sorted(self.get_dense_cells(), key=lambda x: random.random())
        self.live_cells.update(p[:num_cells])

    def live_cell_count(self):
        return len(self.live_cells)

    def gen_all_neighbors(self):
        """Generate all neighbored cells of live cells."""
        for (cr, cc) in self.live_cells:
            for dr, dc in self.neighbors_map:
                yield (cr + dr, cc + dc)

    def get_neighbor_counts(self):
        ncs = {}
        for n in self.gen_all_neighbors():
            ncs[n] = 1 + ncs.get(n, 0)
        return ncs

    def advance(self):
        nc = self.get_neighbor_counts()
        to_die = set(lc for lc in self.live_cells if nc.get(lc, 0) not in [2, 3])
        to_birth = set(dc for dc in set(nc) - set(self.live_cells) if nc.get(dc, 0) == 3)
        self.live_cells = (self.live_cells - to_die | to_birth) & self.get_dense_cells()


def main():
    mygame = GameOfLife(rows=3, cols=3)  # setup the board
    random.seed(0)
    mygame.seed(10)
    mygame.dump()
    for iturn in range(50):
        if 0 == mygame.live_cell_count():
            print("All cells are dead, game over.")
            break
        made_changes = mygame.advance()
        mygame.dump()
        if made_changes is False:
            print("Reached a steady state, game over.")
            break
        time.sleep(0.1)


if "__main__" == __name__:
    main()
