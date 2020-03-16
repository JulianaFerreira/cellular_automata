from tkinter import *
import random
import copy
import matplotlib.pylab as plt
import imageio as imageio
from PIL import Image, ImageGrab
import numpy as np

# States - quality
qualityStates = ["Good", "Medium", "Bad", "Dead"]
# Transition matrix - quality
qualityTransitionMatrix = [[0.6, 0.3, 0.1, 0], [0.2, 0.6, 0.2, 0], [0.3, 0.495, 0.195, 0.01], [0, 0, 0, 1]]
qualityTransitionMatrixGood = [[0.7, 0.25, 0.05, 0], [0.3, 0.55, 0.15, 0], [0.4, 0.445, 0.145, 0.01], [0, 0, 0, 1]]
qualityTransitionMatrixMed = [[0.55, 0.4, 0.05, 0], [0.15, 0.7, 0.15, 0], [0.25, 0.595, 0.145, 0.01], [0, 0, 0, 1]]
qualityTransitionMatrixBad = [[0.55, 0.25, 0.2, 0], [0.15, 0.55, 0.3, 0], [0.25, 0.445, 0.295, 0.01], [0, 0, 0, 1]]

# States - weather
weatherStates = ["Sun", "Rain"]
# Transition matrix - weather
weatherTransitionMatrix = [[0.8, 0.2], [0.7, 0.3]]

time = 480
cycles = 32
timeinterval = 15

# Size
width = 30
height = 40
quantCells = width * height

good = []
medium = []
bad = []
dead = []


class Cell:

    def __init__(self, time, quality, phase, weather):
        self.time = time
        self.quality = quality
        self.phase = phase
        self.weather = weather

    def gettime(self):
        return self.time

    def settime(self, time):
        self.time = time

    def getquality(self):
        return self.quality

    def setquality(self, quality):
        self.quality = quality

    def getphase(self):
        return self.phase

    def setphase(self, phase):
        self.phase = phase

    def getweather(self):
        return self.weather

    def setweather(self, weather):
        self.weather = weather


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

    good_line, = plt.plot(good, label='Good')
    medium_line, = plt.plot(medium, label='Medium')
    bad_line, = plt.plot(bad, label='Bad')
    dead_line, = plt.plot(dead, label='Dead')

    plt.legend(handles=[good_line, medium_line, bad_line, dead_line])

    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    plt.xlabel('Transition')
    plt.ylabel('Cells')

    plt.savefig('myplot.png')
    plt.show()


def put_cells():
    # state: 0 = good, 1 = medium, 2 = bad, 3 = dead
    # phase: 0 = bud, 1 = tillering, 2 = grow, 3 = mature, 4 = harvest
    # weather: 0 = sun, 1 = rain
    # Initial quantity cell: Good - 9; Medium - 10; Bad - 1  / Sun - 15; Rain - 5
    aleatory_cells = [Cell(0, qualityStates[1], 0, weatherStates[0]), Cell(0, qualityStates[0], 0, weatherStates[0]),
                      Cell(0, qualityStates[0], 0, weatherStates[0]), Cell(0, qualityStates[1], 0, weatherStates[0]),
                      Cell(0, qualityStates[0], 0, weatherStates[0]), Cell(0, qualityStates[1], 0, weatherStates[1]),
                      Cell(0, qualityStates[0], 0, weatherStates[0]), Cell(0, qualityStates[1], 0, weatherStates[0]),
                      Cell(0, qualityStates[1], 0, weatherStates[0]), Cell(0, qualityStates[2], 0, weatherStates[0]),
                      Cell(0, qualityStates[0], 0, weatherStates[1]), Cell(0, qualityStates[1], 0, weatherStates[1]),
                      Cell(0, qualityStates[0], 0, weatherStates[0]), Cell(0, qualityStates[0], 0, weatherStates[0]),
                      Cell(0, qualityStates[0], 0, weatherStates[0]), Cell(0, qualityStates[1], 0, weatherStates[0]),
                      Cell(0, qualityStates[1], 0, weatherStates[0]), Cell(0, qualityStates[1], 0, weatherStates[1]),
                      Cell(0, qualityStates[0], 0, weatherStates[0]), Cell(0, qualityStates[1], 0, weatherStates[1])]

    for y in range(-1, width + 1):
        for x in range(-1, height + 1):
            previousGen[x][y] = random.choice(aleatory_cells)
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
            neighbors_state_good = search_state("Good", x, y)
            neighbors_state_med = search_state("Medium", x, y)
            neighbors_state_bad = search_state("Bad", x, y)
            neighbors = [neighbors_state_good,neighbors_state_med,neighbors_state_bad]
            transitionMatrix = updateTransitionMatrix(qualityTransitionMatrix, neighbors)

            temporary[x][y] = copy.copy(previousGen[x][y])
            temporary[x][y].settime(temporary[x][y].gettime() + timeinterval)

            # setphase
            if previousGen[x][y].gettime() == 30:
                temporary[x][y].setphase(1)

            elif previousGen[x][y].gettime() == 150:
                temporary[x][y].setphase(2)

            elif previousGen[x][y].gettime() == 270:
                temporary[x][y].setphase(3)

            elif previousGen[x][y].gettime() == 480:
                temporary[x][y].setphase(4)


            # Next state - quality
            temporary[x][y].setquality(getNewState(qualityStates, transitionMatrix, previousGen[x][y].getquality()))
            # Next state - weather
            temporary[x][y].setweather(getNewState(weatherStates, weatherTransitionMatrix, previousGen[x][y].getweather()))


            #count states - quality
            if previousGen[x][y].getquality() == qualityStates[0]:
                cells_state_0 += 1
            elif previousGen[x][y].getquality() == qualityStates[1]:
                cells_state_1 += 1
            elif previousGen[x][y].getquality() == qualityStates[2]:
                cells_state_2 += 1
            elif previousGen[x][y].getquality() == qualityStates[3]:
                cells_state_3 += 1

            # count states - weather
            if previousGen[x][y].getweather() == weatherStates[0]:
                cells_sun += 1
            elif previousGen[x][y].getweather() == weatherStates[1]:
                cells_rain += 1



    archive = open("ac.txt", "a")
    archive2 = open("ac.txt", "r")
    content = archive2.readlines()
    archive.write("day: %d" % temporary[0][0].gettime() + "\n")
    archive.write("----------------------------" + "\n")
    archive.write("cells good: %d" % cells_state_0 + "\n")
    archive.write("cells medium: %d" % cells_state_1 + "\n")
    archive.write("cells bad: %d" % cells_state_2 + "\n")
    archive.write("cells dead: %d" % cells_state_3 + "\n")
    archive.write("----------------------------" + "\n")
    archive.write("weather sun: %d" % cells_sun + "\n")
    archive.write("weather rain: %d" % cells_rain + "\n")
    archive.write("----------XXXXX------------" + "\n")
    good.append(cells_state_0)
    medium.append(cells_state_1)
    bad.append(cells_state_2)
    dead.append(cells_state_3)

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
        newTransitionMatrix = qualityTransitionMatrixGood
    elif neighbors[1] > 4:
        newTransitionMatrix = qualityTransitionMatrixMed
    elif neighbors[1] > 4:
        newTransitionMatrix = qualityTransitionMatrixBad

    return newTransitionMatrix



def search_state(state, a, b):
    count = 0

    if previousGen[a - 1][b + 1].getquality() == state:
        count += 1

    if previousGen[a][b + 1].getquality() == state:
        count += 1

    if previousGen[a + 1][b + 1].getquality() == state:
        count += 1

    if previousGen[a - 1][b].getquality() == state:
        count += 1

    if previousGen[a + 1][b].getquality() == state:
        count += 1

    if previousGen[a - 1][b - 1].getquality() == state:
        count += 1

    if previousGen[a][b - 1].getquality() == state:
        count += 1

    if previousGen[a + 1][b - 1].getquality() == state:
        count += 1

    return count

def paint_cells():
    for y in range(width):
        for x in range(height):
            if previousGen[x][y].getquality() == qualityStates[0]:
                canvas.itemconfig(cell[x][y], fill="green")
            elif previousGen[x][y].getquality() == qualityStates[1]:
                canvas.itemconfig(cell[x][y], fill="yellow")
            elif previousGen[x][y].getquality() == qualityStates[2]:
                canvas.itemconfig(cell[x][y], fill="red")
            elif previousGen[x][y].getquality() == qualityStates[3]:
                canvas.itemconfig(cell[x][y], fill="black")


def paint_cells_weather():
    for y in range(width):
        for x in range(height):
            if previousGen[x][y].getweather() == weatherStates[0]:
                canvas.itemconfig(cell[x][y], fill="yellow")
            elif previousGen[x][y].getweather() == weatherStates[1]:
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

# for i in range(0, cycles):
#     processing() #just numbers
#     print("interation:", i)
#
# make_graph()

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