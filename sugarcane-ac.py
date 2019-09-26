from tkinter import *
import random
import copy


class Cell:

    def __init__(self, time, state, phase):
        self.time = time
        self.state = state
        self.phase = phase

    def gettime(self):
        return self.time

    def settime(self, time):
        self.time = time

    def getstate(self):
        return self.state

    def setstate(self, state):
        self.state = state

    def getphase(self):
        return self.phase

    def setphase(self, phase):
        self.phase = phase


cell = [[0 for row in range(-1, 61)] for col in range(-1, 81)]
firstGen = [[0 for row in range(-1, 61)] for col in range(-1, 81)]
temporary = [[0 for row in range(-1, 61)] for col in range(-1, 81)]


def make_frames():
    processing()
    paint_cells()
    root.after(1000, make_frames)


def put_cells():
    # state: 0 = good, 1 = medium, 2 = bad
    # quality score: good: 7-10; medium: 5-7; bad: 0-5
    # phase: 0 = bud, 1 = tillering, 2 = grow, 3 = mature, 4 = harvest, 5 = dead
    aleatory_cells = [Cell(0, 0, 0), Cell(0, 0, 0), Cell(0, 0, 0), Cell(0, 0, 0), Cell(0, 0, 0),
                      Cell(0, 0, 0), Cell(0, 0, 0), Cell(0, 0, 0), Cell(0, 1, 0), Cell(0, 2, 0),
                      Cell(0, 0, 0), Cell(0, 1, 0), Cell(0, 0, 0), Cell(0, 0, 0), Cell(0, 0, 0),
                      Cell(0, 1, 0), Cell(0, 0, 0), Cell(0, 1, 0), Cell(0, 0, 0), Cell(0, 1, 0)]

    for y in range(-1, 61):
        for x in range(-1, 81):
            firstGen[x][y] = random.choice(aleatory_cells)
            temporary[x][y] = 0
            cell[x][y] = canvas.create_rectangle((x * 10, y * 10, x * 10 + 10, y * 10 + 10), outline="gray50", fill="white")


def processing():
    cells_state_0 = 0
    cells_state_1 = 0
    cells_state_2 = 0

    for y in range(0, 60):
        for x in range(0, 80):
            infected_neighbors_state1 = search_neigh_state1(x, y)
            infected_neighbors_state2 = search_neigh_state2(x, y)
            aleatory_cells = [Cell(0, 0, 0), Cell(0, 0, 0), Cell(0, 0, 0), Cell(0, 0, 0), Cell(0, 0, 0),
                              Cell(0, 0, 0), Cell(0, 0, 0), Cell(0, 0, 0), Cell(0, 1, 0), Cell(0, 2, 0),
                              Cell(0, 0, 0), Cell(0, 1, 0), Cell(0, 0, 0), Cell(0, 0, 0), Cell(0, 0, 0),
                              Cell(0, 1, 0), Cell(0, 0, 0), Cell(0, 1, 0), Cell(0, 0, 0), Cell(0, 1, 0)]


            if firstGen[x][y].gettime() > 12:
                temporary[x][y] = random.choice(aleatory_cells)

            else:
                if firstGen[x][y].getstate() == 0:
                    cells_state_0 += 1
                    if (infected_neighbors_state1 > 3 or infected_neighbors_state2 > 2):
                        temporary[x][y] = copy.copy(firstGen[x][y])
                        temporary[x][y].setstate(1)
                    elif infected_neighbors_state1 > 4 or infected_neighbors_state2 > 3:
                        temporary[x][y] = copy.copy(firstGen[x][y])
                        temporary[x][y].setstate(1)
                    else:
                        temporary[x][y] = copy.copy(firstGen[x][y])

                elif firstGen[x][y].getstate() == 1:
                    cells_state_1 += 1
                    if firstGen[x][y].gettime() == 5:
                        temporary[x][y] = copy.copy(firstGen[x][y])
                        temporary[x][y].setstate(2)
                        temporary[x][y].settime(firstGen[x][y].gettime() + 1)
                    else:
                        temporary[x][y] = copy.copy(firstGen[x][y])
                        temporary[x][y].settime(temporary[x][y].gettime() + 1)

                elif firstGen[x][y].getstate() == 2:
                    cells_state_2 += 1
                    if firstGen[x][y].gettime() > 8:
                        temporary[x][y] = copy.copy(firstGen[x][y])
                        temporary[x][y].setstate(1)
                        temporary[x][y].settime(temporary[x][y].gettime() + 1)
                    else:
                        temporary[x][y] = copy.copy(firstGen[x][y])
                        temporary[x][y].settime(temporary[x][y].gettime() + 1)

    archive = open("info.txt", "a")
    archive2 = open("info.txt", "r")
    content = archive2.readlines()
    number_of_lines = len(content)
    archive.write("mounth: %d" % ((number_of_lines / 8) + 1) + "\n")
    archive.write("cells good: %d" % cells_state_0 + "\n")
    archive.write("cells medium: %d" % cells_state_1 + "\n")
    archive.write("cells bad: %d" % cells_state_2 + "\n")
    archive.write("----------------------------" + "\n")

    for y in range(0, 60):
        for x in range(0, 80):
            firstGen[x][y] = temporary[x][y]


def search_neigh_state1(a, b):
    neigh_state1 = 0

    if firstGen[a - 1][b + 1].getstate() == 1:
        neigh_state1 += 1

    if firstGen[a][b + 1].getstate() == 1:
        neigh_state1 = neigh_state1 + 1

    if firstGen[a + 1][b + 1].getstate() == 1:
        neigh_state1 = neigh_state1 + 1

    if firstGen[a - 1][b].getstate() == 1:
        neigh_state1 = neigh_state1 + 1

    if firstGen[a + 1][b].getstate() == 1:
        neigh_state1 = neigh_state1 + 1

    if firstGen[a - 1][b - 1].getstate() == 1:
        neigh_state1 = neigh_state1 + 1

    if firstGen[a][b - 1].getstate() == 1:
        neigh_state1 = neigh_state1 + 1

    if firstGen[a + 1][b - 1].getstate() == 1:
        neigh_state1 = neigh_state1 + 1

    return neigh_state1


def search_neigh_state2(a, b):
    neigh_state2 = 0

    if firstGen[a - 1][b + 1].getstate() == 2:
        neigh_state2 += 1

    if firstGen[a][b + 1].getstate() == 2:
        neigh_state2 += 1

    if firstGen[a + 1][b + 1].getstate() == 2:
        neigh_state2 += 1

    if firstGen[a - 1][b].getstate() == 2:
        neigh_state2 += 1

    if firstGen[a + 1][b].getstate() == 2:
        neigh_state2 += 1

    if firstGen[a - 1][b - 1].getstate() == 2:
        neigh_state2 += 1

    if firstGen[a][b - 1].getstate() == 2:
        neigh_state2 += 1

    if firstGen[a + 1][b - 1].getstate() == 2:
        neigh_state2 += 1

    return neigh_state2


def paint_cells():
    for y in range(60):
        for x in range(80):
            if firstGen[x][y].getstate() == 0:
                canvas.itemconfig(cell[x][y], fill="green")
            if firstGen[x][y].getstate() == 1:
                canvas.itemconfig(cell[x][y], fill="yellow")
            if firstGen[x][y].getstate() == 2:
                canvas.itemconfig(cell[x][y], fill="red")


root = Tk()
canvas = Canvas(root, width=800, height=600, highlightthickness=0, bd=0, bg='white')
canvas.pack()
put_cells()

make_frames()
root.mainloop()
