from tkinter import *
import random
import copy
import matplotlib.pylab as plt
import imageio as imageio
from PIL import Image, ImageGrab
import numpy as np

# States - quality
states1 = ["Good", "Medium", "Bad", "Dead"]
# Initial Probability
probability1 = [0.45, 0.5, 0.05, 0]
# Transition matrix - quality
transitionMatrix1 = [[0.6, 0.3, 0.1, 0], [0.2, 0.6, 0.2, 0], [0.3, 0.495, 0.195, 0.01], [0, 0, 0, 1]]
transitionMatrix11 = [[0.7, 0.25, 0.05, 0], [0.3, 0.55, 0.15, 0], [0.4, 0.445, 0.145, 0.01], [0, 0, 0, 1]]
transitionMatrix12 = [[0.55, 0.4, 0.05, 0], [0.15, 0.7, 0.15, 0], [0.25, 0.595, 0.145, 0.01], [0, 0, 0, 1]]
transitionMatrix13 = [[0.55, 0.25, 0.2, 0], [0.15, 0.55, 0.3, 0], [0.25, 0.445, 0.295, 0.01], [0, 0, 0, 1]]

# States - weather
states2 = ["Sun", "Rain"]
# Initial Probability
probability2 = [0.75, 0.25]
# Transition matrix - weather
transitionMatrix2 = [[0.8, 0.2], [0.7, 0.3]]

time = 480
cycles = 32
timeinterval = 15

# Size
width = 30
height = 40
quantCells = width * height

quantityState0 = []
quantityState1 = []
quantityState2 = []
quantityState3 = []


class Cell:

    def __init__(self, time, state1, state2, state3):
        self.time = time
        self.state1 = state1
        self.state2 = state2
        self.state3 = state3

    def gettime(self):
        return self.time

    def settime(self, time):
        self.time = time

    def getstate1(self):
        return self.state1

    def setstate1(self, state1):
        self.state1 = state1

    def getstate2(self):
        return self.state2

    def setstate2(self, state2):
        self.state2 = state2

    def getstate3(self):
        return self.state3

    def setstate3(self, state3):
        self.state3 = state3


cell = [[0 for row in range(-1, width + 1)] for col in range(-1, height + 1)]
previousGen = [[0 for row in range(-1, width + 1)] for col in range(-1, height + 1)]
temporary = [[0 for row in range(-1, width + 1)] for col in range(-1, height + 1)]


def make_frames():
    processing()
    paint_cells()
    #paint_cells_phase()
    #paint_cells_weather()
    root.update()  # comment to make infinite
    # root.after(1000, make_frames) #not comment to make infinite


def make_graph():
    figure = plt.figure()
    plt.title('Sugarcane Quality')
    # t = np.linspace(0, time, time)
    # np.arange(0.0, quantCells, 1.0)

    s1_line, = plt.plot(quantityState0, label=states1[0], color="green")
    s2_line, = plt.plot(quantityState1, label=states1[1], color="yellow")
    s3_line, = plt.plot(quantityState2, label=states1[2], color="red")
    s4_line, = plt.plot(quantityState3, label=states1[3], color="black")

    plt.legend(handles=[s1_line, s2_line, s3_line, s4_line])

    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    plt.xlabel('Transition')
    plt.ylabel('Cells')

    plt.savefig('myplot.png')
    plt.show()


def put_cells():
    for y in range(-1, width + 1):
        for x in range(-1, height + 1):
            state1 = np.random.choice(states1, replace=True, p=probability1)
            state2 = np.random.choice(states2, replace=True, p=probability2)
            #state3 = np.random.choice(states3, replace=True, p=probability3)
            newCell = Cell(0, state1, state2, 0)
            previousGen[x][y] = newCell
            temporary[x][y] = 0
            cell[x][y] = canvas.create_rectangle((x * 20, y * 20, x * 20 + 20, y * 20 + 20), outline="gray50",
                                                 fill="white")


def processing():
    cells_state_0 = 0
    cells_state_1 = 0
    cells_state_2 = 0
    cells_state_3 = 0
    cells_sun = 0
    cells_rain = 0

    for y in range(0, width):
        for x in range(0, height):
            neighbors_state1 = search_state(states1[0], x, y)
            neighbors_state2 = search_state(states1[1], x, y)
            neighbors_state3 = search_state(states1[2], x, y)
            neighbors = [neighbors_state1, neighbors_state2, neighbors_state3]
            transitionMatrix = updateTransitionMatrix(transitionMatrix1, neighbors)

            temporary[x][y] = copy.copy(previousGen[x][y])
            temporary[x][y].settime(temporary[x][y].gettime() + timeinterval)

            # Next state - quality
            temporary[x][y].setstate1(getNewState(states1, transitionMatrix1, previousGen[x][y].getstate1()))
            # Next state - weather
            temporary[x][y].setstate2(getNewState(states2, transitionMatrix2, previousGen[x][y].getstate2()))

            #count state
            if previousGen[x][y].getstate1() == states1[0]:
                cells_state_0 += 1
            elif previousGen[x][y].getstate1() == states1[1]:
                cells_state_1 += 1
            elif previousGen[x][y].getstate1() == states1[2]:
                cells_state_2 += 1
            elif previousGen[x][y].getstate1() == states1[3]:
                cells_state_3 += 1

            # count states - weather
            if previousGen[x][y].getstate2() == states2[0]:
                cells_sun += 1
            elif previousGen[x][y].getstate2() == states2[1]:
                cells_rain += 1



    archive = open("ac.txt", "a")
    archive2 = open("ac.txt", "r")
    content = archive2.readlines()
    archive.write("day: %d" % temporary[0][0].gettime() + "\n")
    archive.write("----------------------------" + "\n")
    archive.write("cells state " + states1[0] + ": %d" % cells_state_0 + "\n")
    archive.write("cells state " + states1[1] + ": %d" % cells_state_1 + "\n")
    archive.write("cells state " + states1[2] + ": %d" % cells_state_2 + "\n")
    archive.write("cells state " + states1[3] + ": %d" % cells_state_3 + "\n")
    archive.write("----------------------------" + "\n")
    archive.write("weather sun: %d" % cells_sun + "\n")
    archive.write("weather rain: %d" % cells_rain + "\n")
    archive.write("----------XXXXX------------" + "\n")
    quantityState0.append(cells_state_0)
    quantityState1.append(cells_state_1)
    quantityState2.append(cells_state_2)
    quantityState3.append(cells_state_3)

    for y in range(0, width):
        for x in range(0, height):
            previousGen[x][y] = temporary[x][y]


# Function that implements the Markov model
def getNewState(states, transitionMatrix, currentState):
    i = 0
    newState = ""
    for x in states:
        if currentState == x:
            newState = np.random.choice(states, replace=True, p=transitionMatrix[i])
        i+=1

    return newState


def updateTransitionMatrix(transitionMatrix, neighbors):
    newTransitionMatrix = transitionMatrix

    if neighbors[0] > 4:
        newTransitionMatrix = transitionMatrix11
    elif neighbors[1] > 4:
        newTransitionMatrix = transitionMatrix12
    elif neighbors[1] > 4:
        newTransitionMatrix = transitionMatrix13

    return newTransitionMatrix


def search_state(state, a, b):
    count = 0

    if previousGen[a - 1][b + 1].getstate1() == state:
        count += 1

    if previousGen[a][b + 1].getstate1() == state:
        count += 1

    if previousGen[a + 1][b + 1].getstate1() == state:
        count += 1

    if previousGen[a - 1][b].getstate1() == state:
        count += 1

    if previousGen[a + 1][b].getstate1() == state:
        count += 1

    if previousGen[a - 1][b - 1].getstate1() == state:
        count += 1

    if previousGen[a][b - 1].getstate1() == state:
        count += 1

    if previousGen[a + 1][b - 1].getstate1() == state:
        count += 1

    return count


def paint_cells():
    for y in range(width):
        for x in range(height):
            if previousGen[x][y].getstate1() == states1[0]:
                canvas.itemconfig(cell[x][y], fill="green")
            elif previousGen[x][y].getstate1() == states1[1]:
                canvas.itemconfig(cell[x][y], fill="yellow")
            elif previousGen[x][y].getstate1() == states1[2]:
                canvas.itemconfig(cell[x][y], fill="red")
            elif previousGen[x][y].getstate1() == states1[3]:
                canvas.itemconfig(cell[x][y], fill="black")

def paint_cells_weather():
    for y in range(width):
        for x in range(height):
            if previousGen[x][y].getstate2() == states2[0]:
                canvas.itemconfig(cell[x][y], fill="yellow")
            elif previousGen[x][y].getstate2() == states2[1]:
                canvas.itemconfig(cell[x][y], fill="blue")

def paint_cells_phase():
    for y in range(width):
        for x in range(height):
            if previousGen[x][y].getphase() == 0:
                canvas.itemconfig(cell[x][y], fill="#f9eebd")
            elif previousGen[x][y].getphase() == 1:
                canvas.itemconfig(cell[x][y], fill="#e7f9bd")
            elif previousGen[x][y].getphase() == 2:
                canvas.itemconfig(cell[x][y], fill="#c2f7a8")
            elif previousGen[x][y].getphase() == 3:
                canvas.itemconfig(cell[x][y], fill="#56fc2d")
            elif previousGen[x][y].getphase() == 4:
                canvas.itemconfig(cell[x][y], fill="#f9ccbd")

root = Tk()
# Original size 800 x 600
canvas = Canvas(root, width=800, height=600, highlightthickness=0, bd=0, bg='white')
canvas.pack()
put_cells()

images = []

#just numbers
# for i in range(0, cycles):
#     processing()
#     print("interation:", i)
#
# make_graph()

#image CA
for i in range(0, cycles):  # comment to make infinite
    make_frames()
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    xx = x + canvas.winfo_width()
    yy = y + canvas.winfo_height()
    images.append(ImageGrab.grab((x, y, xx, yy)))

make_graph()

imageio.mimsave('ac.gif', images, duration=0.5)

root.mainloop()