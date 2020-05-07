#!/usr/bin/env python

# game of life
# no conditionals (no if's)
# no mutables (tuples, frozenset... )

# sparse representation / dense representation
# if => {True: func_if_true, False: func_if_false}[condition](args)
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


def no_op(*args, **kwargs):
    pass


class GameOfLife:
    LIVE = 1
    DEAD = 0

    def __init__(self, rows=4, cols=4):
        def raise_error_for_valid_size():
            raise AssertionError("Must have both rows and cols!")
        {
            True: raise_error_for_valid_size,
            False: no_op,
        }[min(rows, cols) < 1]()
        self.dimensions = (rows, cols)
        self.cell_states = []
        self.live_neighbor_counts = []
        self.zero_out()

        # move like a king
        # make a set of the 3x3 grid centered at origin
        self.neighbors_map = set(
            itertools.product(
                range(-1,2),
                range(-1,2)
            )
        )
        # remove (0,0)
        self.neighbors_map.remove((0,0))


    def zero_out(self):
        # reset board to correct size and fill in with dead cells and everyone
        # has zero live neighbors
        self.cell_states[:] = []
        self.live_neighbor_counts[:] = []
        for rownum in range(self.dimensions[0]):
            self.cell_states.append([])
            self.live_neighbor_counts.append([])
            for colnum in range(self.dimensions[1]):
                self.cell_states[-1].append(self.DEAD)
                self.live_neighbor_counts[-1].append(0)

    def dump(self):
        width = 5 + 3 * self.dimensions[0]
        print("Cell states:")
        pprint.pprint(self.cell_states, width=width)

        # print("Neighbor counts:")
        # pprint.pprint(self.live_neighbor_counts, width=width)

    def seed(self, num_cells):
        """Starting with a zero'd out map, toggle num_cells on (or make best effort)"""
        # if someone tries to turn on more cells than are currently turned off, what to do?
        dead_cells = self.get_dead_cells()
        if False:
            try:
                dead_cells[num_cells]
            except IndexError:
                raise AssertionError("Can't turn on that many cells")
        random.shuffle(dead_cells)
        to_toggle_on = dead_cells[:num_cells]
        for proposed_row, proposed_col in to_toggle_on:
            self.cell_states[proposed_row][proposed_col] = self.LIVE
        self.init_neighbors()

    def live_cell_count(self):
        total = 0
        for irow in self.cell_states:
            total += sum(irow)
        return total

    def get_dead_cells(self):
        return list(
            filter(
                lambda row_col: self.cell_states[row_col[0]][row_col[1]] is self.DEAD,
                ( # begin generator
                    (rownum, colnum)
                    for rownum in range(self.dimensions[0])
                    for colnum in range(self.dimensions[1])
                ) # end of generator
            )
        )


    def delta_neighbors(self, rowidx, colidx, step=0):
        try:
            {
                -1: True,
                1: True,
            }[step]
        except KeyError:
            raise AssertionError("can only increment or decrement")

        maxrow = self.dimensions[0]
        maxcol = self.dimensions[1]

        # replace nested loops with single loop over neighbors map
        for neighbor in self.neighbors_map:
            rowoffset, coloffset = neighbor
            newrow = rowidx + rowoffset
            newcol = colidx + coloffset
            not_below = (0 <= newrow) and (0 <= newcol)
            not_above = (newrow < maxrow) and (newcol < maxcol)
            computed_step = step * not_below * not_above
            try:
                {
                    0: no_op,
                }[computed_step]
            except KeyError:
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
                {
                    self.LIVE: self.increment_neighbors,
                    self.DEAD: no_op,
                }[cell_state](rowidx, colidx)

    def advance(self):
        # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        # Any live cell with more than three live neighbours dies, as if by overpopulation.
        # Any dead cell with exactly three live neighbours becomes a live cell,
        # as if by reproduction.
        to_birth = []
        to_die = []

        def live_action(rowidx, colidx, cell_neighor_count):
            # cell_neighbor_count [0, 8], [0, 9)
            def kill_this_cell(r, c):
                to_die.append((r, c))

            action_map = {n: kill_this_cell for n in range(0, 9)}
            for i in [2, 3]:
                action_map[i] = no_op
            action_map[cell_neighbor_count](rowidx, colidx)


        def dead_action(rowidx, colidx, cell_neighbor_count):
            def birth_this_cell(r, c):
                to_birth.append((r,c))
            action_map = {n: no_op for n in range(0, 9)}
            action_map[3] = birth_this_cell
            action_map[cell_neighbor_count](rowidx, colidx)

        for rowidx, irow in enumerate(self.cell_states):
            for colidx, cell_state in enumerate(irow):
                cell_neighbor_count = self.live_neighbor_counts[rowidx][colidx]
                {
                    self.LIVE: live_action,
                    self.DEAD: dead_action,
                }[cell_state](rowidx, colidx, cell_neighbor_count)

        # birth cells
        for rowidx, colidx in to_birth:
            self.cell_states[rowidx][colidx] = self.LIVE
            self.increment_neighbors(rowidx, colidx)

        # death cells
        for rowidx, colidx in to_die:
            self.cell_states[rowidx][colidx] = self.DEAD
            self.decrement_neighbors(rowidx, colidx)

        # return the boolean of were any changes made
        return bool(to_die) or bool(to_birth)


def main():
    mygame = GameOfLife()  # setup the board
    random.seed(0)
    mygame.seed(17)
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
