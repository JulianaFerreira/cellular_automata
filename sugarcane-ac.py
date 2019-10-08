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
    root.update()
    #root.after(1000, make_frames)


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
            neighbors_state0 = search_state0(x, y)
            neighbors_state1 = search_state1(x, y)
            neighbors_state2 = search_state2(x, y)

            temporary[x][y] = copy.copy(firstGen[x][y])
            temporary[x][y].settime(temporary[x][y].gettime() + 15)

            #setphase
            if firstGen[x][y].getphase() == 30:
                firstGen[x][y].setphase(1)

            elif firstGen[x][y].getphase() == 150:
                firstGen[x][y].setphase(2)

            elif firstGen[x][y].getphase() == 270:
                firstGen[x][y].setphase(3)

            elif firstGen[x][y].getphase() == 480:
                firstGen[x][y].setphase(4)


            #setstate
            if firstGen[x][y].getstate() == 0:
                cells_state_0 += 1
                if (neighbors_state1 > 3 or neighbors_state2 > 2): #and firstGen[x][y].getphase() == 0:
                    temporary[x][y].setstate(1)
                elif neighbors_state1 > 2 or neighbors_state2 > 3:
                    temporary[x][y].setstate(2)

            elif firstGen[x][y].getstate() == 1:
                cells_state_1 += 1
                if neighbors_state0 > 4:  # and firstGen[x][y].getphase() == 0:
                    temporary[x][y].setstate(0)
                elif neighbors_state0 > 2 or neighbors_state2 > 3:
                    temporary[x][y].setstate(2)

            elif firstGen[x][y].getstate() == 2:
                cells_state_2 += 1
                if neighbors_state0 > 4:  # and firstGen[x][y].getphase() == 0:
                    temporary[x][y].setstate(0)
                elif neighbors_state0 > 2 or neighbors_state1 > 3:
                    temporary[x][y].setstate(1)


    archive = open("ac.txt", "a")
    archive2 = open("ac.txt", "r")
    content = archive2.readlines()
    number_of_lines = len(content)
    archive.write("dias: %d" % temporary[0][0].gettime() + "\n")
    archive.write("cells good: %d" % cells_state_0 + "\n")
    archive.write("cells medium: %d" % cells_state_1 + "\n")
    archive.write("cells bad: %d" % cells_state_2 + "\n")
    archive.write("----------------------------" + "\n")

    for y in range(0, 60):
        for x in range(0, 80):
            firstGen[x][y] = temporary[x][y]


def search_state0(a, b):
    state0 = 0

    if firstGen[a - 1][b + 1].getstate() == 0:
        state0 += 1

    if firstGen[a][b + 1].getstate() == 0:
        state0 += 1

    if firstGen[a + 1][b + 1].getstate() == 0:
        state0 += 1

    if firstGen[a - 1][b].getstate() == 0:
        state0 += 1

    if firstGen[a + 1][b].getstate() == 0:
        state0 += 1

    if firstGen[a - 1][b - 1].getstate() == 0:
        state0 += 1

    if firstGen[a][b - 1].getstate() == 0:
        state0 += 1

    if firstGen[a + 1][b - 1].getstate() == 0:
        state0 += 1

    return state0

def search_state1(a, b):
    state1 = 0

    if firstGen[a - 1][b + 1].getstate() == 1:
        state1 += 1

    if firstGen[a][b + 1].getstate() == 1:
        state1 += 1

    if firstGen[a + 1][b + 1].getstate() == 1:
        state1 += 1

    if firstGen[a - 1][b].getstate() == 1:
        state1 += 1

    if firstGen[a + 1][b].getstate() == 1:
        state1 += 1

    if firstGen[a - 1][b - 1].getstate() == 1:
        state1 += 1

    if firstGen[a][b - 1].getstate() == 1:
        state1 += 1

    if firstGen[a + 1][b - 1].getstate() == 1:
        state1 += 1

    return state1


def search_state2(a, b):
    state2 = 0

    if firstGen[a - 1][b + 1].getstate() == 2:
        state2 += 1

    if firstGen[a][b + 1].getstate() == 2:
        state2 += 1

    if firstGen[a + 1][b + 1].getstate() == 2:
        state2 += 1

    if firstGen[a - 1][b].getstate() == 2:
        state2 += 1

    if firstGen[a + 1][b].getstate() == 2:
        state2 += 1

    if firstGen[a - 1][b - 1].getstate() == 2:
        state2 += 1

    if firstGen[a][b - 1].getstate() == 2:
        state2 += 1

    if firstGen[a + 1][b - 1].getstate() == 2:
        state2 += 1

    return state2


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

for x in range(0, 32):
    make_frames()

root.mainloop()
