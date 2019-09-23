from tkinter import *
import random
import copy


class Cell:

    def __init__(self, quality, phase):
        self.quality = quality
        self.phase = phase

    def getphase(self):
        return self.phase

    def setphase(self, phase):
        self.phase = phase

    def getquality(self):
        return self.quality

    def setquality(self, quality):
        self.quality = quality

cell = [[0 for row in range(-1, 61)] for col in range(-1, 81)]
firstGen = [[0 for row in range(-1, 61)] for col in range(-1, 81)]
temporary = [[0 for row in range(-1, 61)] for col in range(-1, 81)]


def make_frames():
    processing()
    paint_cells()
    root.after(1000, make_frames)


#TODO alterar variaveis aleatory_cells
def put_cells():
    # quality: 0 = good, 1 = medium, 2 = bad
    # phase: 0 = bud, 1 = tillering, 2 = grow, 3 = mature, 4 = harvest, 5 = dead
    aleatory_cells = [Cell(1, 2, 15, 0), Cell(0, 0, 22, 0), Cell(1, 1, 52, 0), Cell(0, 0, 59, 0), Cell(0, 0, 26, 0),
                      Cell(0, 1, 17, 1), Cell(0, 0, 19, 1), Cell(0, 0, 57, 1), Cell(0, 0, 61, 1), Cell(0, 0, 28, 1),
                      Cell(0, 0, 33, 0), Cell(1, 2, 45, 0), Cell(1, 1, 29, 0), Cell(0, 0, 45, 0), Cell(0, 0, 25, 0),
                      Cell(0, 0, 35, 1), Cell(0, 0, 43, 1), Cell(0, 0, 36, 1), Cell(0, 0, 13, 1), Cell(0, 0, 24, 1)]

    for y in range(-1, 61):
        for x in range(-1, 81):
            firstGen[x][y] = random.choice(aleatory_cells)
            temporary[x][y] = 0
            cell[x][y] = canvas.create_oval((x * 10, y * 10, x * 10 + 10, y * 10 + 10), outline="gray50", fill="black")





#TODO parei aqui
def processing():
    cells_state_0 = 0
    cells_state_1 = 0
    cells_state_2 = 0
    N_young = 0
    young_woman_infected = 0
    young_man_infected = 0

    for y in range(0, 60):
        for x in range(0, 80):
            infected_neighbors_state1 = search_neigh_state1(x, y)
            infected_neighbors_state2 = search_neigh_state2(x, y)
            aleatory_cells = [Cell(1, 2, 15, 0), Cell(0, 0, 22, 0), Cell(1, 1, 52, 0), Cell(0, 0, 59, 0),
                              Cell(0, 0, 26, 0), Cell(0, 1, 17, 1), Cell(0, 0, 19, 1), Cell(0, 0, 57, 1),
                              Cell(0, 0, 61, 1), Cell(0, 0, 28, 1), Cell(0, 0, 33, 0), Cell(1, 2, 45, 0),
                              Cell(1, 1, 29, 0), Cell(0, 0, 45, 0), Cell(0, 0, 25, 0), Cell(0, 0, 35, 1),
                              Cell(0, 0, 43, 1), Cell(0, 0, 36, 1), Cell(0, 0, 13, 1), Cell(0, 0, 24, 1)]
            if 16 <= firstGen[x][y].getage() <= 25:
                N_young += 1
                if (firstGen[x][y].getgender() == 1) and (firstGen[x][y].getstate() == 1 or firstGen[x][y].getstate() == 2):
                    young_woman_infected += 1
                if (firstGen[x][y].getgender() == 0) and (firstGen[x][y].getstate() == 1 or firstGen[x][y].getstate() == 2):
                    young_man_infected += 1


            if firstGen[x][y].getinfect_time() > 12:
                temporary[x][y] = random.choice(aleatory_cells)

            else:
                if firstGen[x][y].getstate() == 0:
                    cells_state_0 += 1
                    if (infected_neighbors_state1 > 3 or infected_neighbors_state2 > 2) and \
                            (16 < firstGen[x][y].getage() > 25):
                        temporary[x][y] = copy.copy(firstGen[x][y])
                        temporary[x][y].setstate(1)
                    elif infected_neighbors_state1 > 4 or infected_neighbors_state2 > 3:
                        temporary[x][y] = copy.copy(firstGen[x][y])
                        temporary[x][y].setstate(1)
                    else:
                        temporary[x][y] = copy.copy(firstGen[x][y])

                elif firstGen[x][y].getstate() == 1:
                    cells_state_1 += 1
                    if firstGen[x][y].getinfect_time() == 5:
                        temporary[x][y] = copy.copy(firstGen[x][y])
                        temporary[x][y].setstate(2)
                        temporary[x][y].setinfect_time(firstGen[x][y].getinfect_time() + 1)
                    else:
                        temporary[x][y] = copy.copy(firstGen[x][y])
                        temporary[x][y].setinfect_time(temporary[x][y].getinfect_time() + 1)

                elif firstGen[x][y].getstate() == 2:
                    cells_state_2 += 1
                    if firstGen[x][y].getinfect_time() > 8:
                        temporary[x][y] = copy.copy(firstGen[x][y])
                        temporary[x][y].setstate(1)
                        temporary[x][y].setinfect_time(temporary[x][y].getinfect_time() + 1)
                    else:
                        temporary[x][y] = copy.copy(firstGen[x][y])
                        temporary[x][y].setinfect_time(temporary[x][y].getinfect_time() + 1)

    archive = open("info.txt", "a")
    archive2 = open("info.txt", "r")
    content = archive2.readlines()
    number_of_lines = len(content)
    archive.write("mounth: %d" % ((number_of_lines / 8) + 1) + "\n")
    print((number_of_lines / 8) + 1)
    archive.write("cells susceptible: %d" % cells_state_0 + "\n")
    archive.write("cells infected: %d" % cells_state_1 + "\n")
    archive.write("cells with symptoms: %d" % cells_state_2 + "\n")
    archive.write("young: %d " % N_young + "\n")
    archive.write("young woman infected: %d " % young_woman_infected + "\n")
    archive.write("young man infected: %d " % young_man_infected + "\n")
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
                canvas.itemconfig(cell[x][y], fill="black")
            if firstGen[x][y].getstate() == 1:
                canvas.itemconfig(cell[x][y], fill="yellow")
            if firstGen[x][y].getstate() == 2:
                canvas.itemconfig(cell[x][y], fill="red")


root = Tk()
canvas = Canvas(root, width=800, height=600, highlightthickness=0, bd=0, bg='black')
canvas.pack()
put_cells()

make_frames()
root.mainloop()
