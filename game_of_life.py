#!/usr/bin/env python
"""
Any live cell with fewer than two live neighbours dies, as if by underpopulation.
Any live cell with two or three live neighbours lives on to the next generation.
Any live cell with more than three live neighbours dies, as if by overpopulation.
Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

So keep track of state of cell (live/dead)
and counts of neighbors (birth of cell increments all neighbors (8) by 1, death of cell decrements live neighbors by 1)
"""

import pprint
import random
import time

LIVE = 1
DEAD = 0

class GameOfLife:
    def __init__(self):
        self.dimensions = (4, 4)
        self.cell_states = []
        self.live_neighbor_counts = []
        self.zero_out()

    def zero_out(self):
        self.cell_states[:] = []
        self.live_neighbor_counts[:] = []
        for rownum in range(self.dimensions[0]):
            self.cell_states.append([])
            self.live_neighbor_counts.append([])
            for colnum in range(self.dimensions[1]):
                self.cell_states[-1].append(DEAD)
                self.live_neighbor_counts[-1].append(0)

    def dump(self):
        width = 5 + 3 * self.dimensions[0]
        print("Cell states:")
        pprint.pprint(self.cell_states, width=width)

        print("Neighbor counts:")
        pprint.pprint(self.live_neighbor_counts, width=width)

    def seed(self, num_cells):
        while num_cells > 0:
            for attempt in range(5):
                proposed_row = random.choice(self.cell_states)
                proposed_col = random.randint(0, len(proposed_row) - 1)
                if proposed_row[proposed_col]:
                    continue
                else:
                    proposed_row[proposed_col] = LIVE
                    break
            else:
                break
            num_cells -= 1
        self.init_neighbors()

    def live_cell_count(self):
        total = 0
        for irow in self.cell_states:
            total += sum(irow)
        return total

    def delta_neighbors(self, rowidx, colidx, step=0):
        if step not in [-1, 1]:
            raise AssertionError("can only increment or decrement")
        maxrow = self.dimensions[0]
        maxcol = self.dimensions[1]
        for rowoffset in [-1, 0, 1]:
            for coloffset in [-1, 0, 1]:
                if (rowoffset, coloffset) == 0:
                    continue
                newrow = rowidx + rowoffset
                newcol = colidx + coloffset
                if newrow < 0 or newcol < 0:
                    continue
                if newrow >= maxrow or newcol >= maxcol:
                    continue
                self.live_neighbor_counts[newrow][newcol] += step

    def increment_neighbors(self, rowidx, colidx):
        return self.delta_neighbors(rowidx, colidx, step=1)

    def decrement_neighbors(self, rowidx, colidx):
        return self.delta_neighbors(rowidx, colidx, step=-1)

    def init_neighbors(self):
        # beware of negative indexes
        # probably zero out everything first
        for irow in self.live_neighbor_counts:
            for icol in range(len(irow)):
                irow[icol] = 0

        for rowidx, irow in enumerate(self.cell_states):
            for colidx, cell_state in enumerate(irow):
                if cell_state:
                    self.increment_neighbors(rowidx, colidx)


    def advance(self):
        # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        # Any live cell with more than three live neighbours dies, as if by overpopulation.
        # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        to_birth = []
        to_die = []
        for rowidx, irow in enumerate(self.cell_states):
            for colidx, cell_state in enumerate(irow):
                cell_neighbor_count = self.live_neighbor_counts[rowidx][colidx]
                if cell_state is LIVE:
                    if cell_neighbor_count < 2:
                        to_die.append((rowidx, colidx))
                    elif 3 < cell_neighbor_count:
                        to_die.append((rowidx, colidx))
                    else:
                        pass
                elif cell_state is DEAD:
                    if 3 == cell_neighbor_count:
                        to_birth.append((rowidx, colidx))
                else:
                    raise AssertionError("Bad cell state")

        # birth cells
        for rowidx, colidx in to_birth:
            self.cell_states[rowidx][colidx] = LIVE
            self.increment_neighbors(rowidx, colidx)

        # death cells
        for rowidx, colidx in to_die:
            self.cell_states[rowidx][colidx] = DEAD
            self.decrement_neighbors(rowidx, colidx)

        # return the boolean of were any changes made
        return bool(to_die) or bool(to_birth)


def main():
    mygame = GameOfLife() # setup the board
    random.seed(0)
    mygame.seed(10)
    mygame.dump()
    for iturn in range(50):
        if 0 == mygame.live_cell_count():
            print("All cells are dead, game over.")
            break
        made_changes = mygame.advance()
        print(made_changes)
        mygame.dump()
        if made_changes is False:
            print("Reached a steady state, game over.")
            break
        time.sleep(0.1)


if "__main__" == __name__:
    main()
