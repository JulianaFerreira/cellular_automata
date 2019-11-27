from tkinter import *
import random
import copy

import imageio as imageio
from PIL import Image, ImageGrab

#test
import numpy as np

# Transition quality
beta = 0.3 #next state
gamma = 0.3 #state before

# Transition weather
sun, rain = 0.7, 0.2

#Size
width = 60
height = 80

class Cell:

    def __init__(self, time, state, phase, weather):
        self.time = time
        self.state = state
        self.phase = phase
        self.weather = weather

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

    def getweather(self):
        return self.weather

    def setweather(self, weather):
        self.weather = weather


cell = [[0 for row in range(-1, width+1)] for col in range(-1, height+1)]
previousGen = [[0 for row in range(-1, width + 1)] for col in range(-1, height + 1)]
temporary = [[0 for row in range(-1, width+1)] for col in range(-1, height+1)]


def make_frames():
    processing()
    paint_cells()
    #paint_cells_phase()
    #paint_cells_weather()
    root.update() #comment to make infinite
    #root.after(1000, make_frames) #not comment to make infinite


def put_cells():
    # state: 0 = good, 1 = medium, 2 = bad, 3 = dead
    # quality score: good: 7-10; medium: 5-7; bad: 0-5
    # phase: 0 = bud, 1 = tillering, 2 = grow, 3 = mature, 4 = harvest
    # weather: 0 = sun, 1 = rain
    # Initial quantity cell: Good - 9; Medium - 10; Bad - 1
    aleatory_cells = [Cell(0, 1, 0, 0), Cell(0, 0, 1, 0), Cell(0, 0, 0, 0), Cell(0, 1, 0, 0), Cell(0, 0, 0, 0),
                      Cell(0, 1, 0, 1), Cell(0, 0, 0, 0), Cell(0, 1, 0, 0), Cell(0, 1, 0, 0), Cell(0, 2, 0, 0),
                      Cell(0, 0, 0, 1), Cell(0, 1, 0, 1), Cell(0, 0, 0, 0), Cell(0, 0, 0, 0), Cell(0, 0, 0, 0),
                      Cell(0, 1, 0, 0), Cell(0, 1, 0, 0), Cell(0, 1, 0, 0), Cell(0, 0, 0, 0), Cell(0, 1, 0, 1)]

    for y in range(-1, width+1):
        for x in range(-1, height+1):
            previousGen[x][y] = random.choice(aleatory_cells)
            temporary[x][y] = 0
            cell[x][y] = canvas.create_rectangle((x * 10, y * 10, x * 10 + 10, y * 10 + 10), outline="gray50", fill="white")


def processing():
    cells_state_0 = 0
    cells_state_1 = 0
    cells_state_2 = 0
    cells_state_3 = 0
    cells_sun = 0
    cells_rain = 0

    for y in range(0, width):
        for x in range(0, height):
            neighbors_state0 = search_state(0, x, y)
            neighbors_state1 = search_state(1, x, y)
            neighbors_state2 = search_state(2, x, y)
            neighbors_sun = search_state(0, x, y)
            neighbors_rain = search_state(1, x, y)

            temporary[x][y] = copy.copy(previousGen[x][y])
            temporary[x][y].settime(temporary[x][y].gettime() + 15)

            #setphase
            if previousGen[x][y].gettime() == 30:
                temporary[x][y].setphase(1)

            elif previousGen[x][y].gettime() == 150:
                temporary[x][y].setphase(2)

            elif previousGen[x][y].gettime() == 270:
                temporary[x][y].setphase(3)

            elif previousGen[x][y].gettime() == 480:
                temporary[x][y].setphase(4)


            #setweather
            if previousGen[x][y].getweather() == 0:
                cells_sun += 1
                temporary[x][y].setweather(getNewWeather(previousGen[x][y].getweather(), neighbors_rain))
            elif previousGen[x][y].getweather() == 1:
                cells_rain += 1
                temporary[x][y].setweather(getNewWeather(previousGen[x][y].getweather(), neighbors_sun))


            #setstate
            if previousGen[x][y].getstate() == 0:
                cells_state_0 += 1
                temporary[x][y].setstate(
                    getNewQuality(previousGen[x][y].getstate(), previousGen[x][y].getweather(), neighbors_state1, neighbors_state2))

            elif previousGen[x][y].getstate() == 1:
                cells_state_1 += 1
                temporary[x][y].setstate(
                    getNewQuality(previousGen[x][y].getstate(), previousGen[x][y].getweather(), neighbors_state0, neighbors_state2))

            elif previousGen[x][y].getstate() == 2:
                cells_state_2 += 1
                temporary[x][y].setstate(
                    getNewQuality(previousGen[x][y].getstate(), previousGen[x][y].getweather(), neighbors_state1, neighbors_state2))

            elif previousGen[x][y].getstate() == 3:
                cells_state_3 += 1


    archive = open("ac.txt", "a")
    archive2 = open("ac.txt", "r")
    content = archive2.readlines()
    archive.write("dia: %d" % temporary[0][0].gettime() + "\n")
    archive.write("----------------------------" + "\n")
    archive.write("cells good: %d" % cells_state_0 + "\n")
    archive.write("cells medium: %d" % cells_state_1 + "\n")
    archive.write("cells bad: %d" % cells_state_2 + "\n")
    archive.write("cells dead: %d" % cells_state_3 + "\n")
    archive.write("----------------------------" + "\n")
    archive.write("weather sun: %d" % cells_sun + "\n")
    archive.write("weather rain: %d" % cells_rain + "\n")
    archive.write("----------XXXXX------------" + "\n")


    for y in range(0, width):
        for x in range(0, height):
            previousGen[x][y] = temporary[x][y]


def search_state(state, a, b):
    count = 0

    if previousGen[a - 1][b + 1].getstate() == state:
        count += 1

    if previousGen[a][b + 1].getstate() == state:
        count += 1

    if previousGen[a + 1][b + 1].getstate() == state:
        count += 1

    if previousGen[a - 1][b].getstate() == state:
        count += 1

    if previousGen[a + 1][b].getstate() == state:
        count += 1

    if previousGen[a - 1][b - 1].getstate() == state:
        count += 1

    if previousGen[a][b - 1].getstate() == state:
        count += 1

    if previousGen[a + 1][b - 1].getstate() == state:
        count += 1

    return count

def search_weather(state, a, b):
    count = 0

    if previousGen[a - 1][b + 1].getweather() == state:
        count += 1

    if previousGen[a][b + 1].getweather() == state:
        count += 1

    if previousGen[a + 1][b + 1].getweather() == state:
        count += 1

    if previousGen[a - 1][b].getweather() == state:
        count += 1

    if previousGen[a + 1][b].getweather() == state:
        count += 1

    if previousGen[a - 1][b - 1].getweather() == state:
        count += 1

    if previousGen[a][b - 1].getweather() == state:
        count += 1

    if previousGen[a + 1][b - 1].getweather() == state:
        count += 1

    return count


def getRandomNumber(distribution):
    if distribution == 0:
        returningRandomNumber = np.random.uniform() # UNIFORM
    elif distribution == 1:
        returningRandomNumber = np.random.normal(.5, .1) # NORMAL
    return returningRandomNumber

def getNewQuality(quality, weather, neighbors_state1, neighbors_state2):
    newBeta = beta
    newGamma = gamma
    newState = quality
    chance = getRandomNumber(0)

    if weather == 0:
        newBeta = newBeta + 0.1
    if weather == 1:
        newGamma = newGamma + 0.1

    if quality == 0: # If G
        if neighbors_state1 > 5 or neighbors_state2 > 6: #M or B close
            if chance < newBeta and chance > 0:
                newState = 1

    elif quality == 1: # If M
        if neighbors_state1 > 4:  # G close
            if chance < newGamma and chance > 0:
                newState = 0
        elif neighbors_state2 > 5:  # B close
            if chance < newBeta and chance > 0:
                newState = 2

    elif quality == 2: # If B
        if neighbors_state1 > 4:  # G close
            if chance < newGamma and chance > 0:
                newState = 1
        elif neighbors_state2 > 5:  # B close
            if chance < newBeta and chance > 0:
                newState = 3

    return newState

def getNewWeather(weather, neighbors_state):
    newState = weather
    chance = getRandomNumber(0)

    if weather == 0: # If Sun
        if neighbors_state > 4:
            if chance < rain and chance > 0:
                newState = 1

    elif weather == 1: # If Rain
        if neighbors_state > 2:
            if chance < sun and chance > 0:
                newState = 0

    return newState


def paint_cells():
    for y in range(width):
        for x in range(height):
            if previousGen[x][y].getstate() == 0:
                canvas.itemconfig(cell[x][y], fill="green")
            elif previousGen[x][y].getstate() == 1:
                canvas.itemconfig(cell[x][y], fill="yellow")
            elif previousGen[x][y].getstate() == 2:
                canvas.itemconfig(cell[x][y], fill="red")
            elif previousGen[x][y].getstate() == 3:
                canvas.itemconfig(cell[x][y], fill="black")

def paint_cells_weather():
    for y in range(width):
        for x in range(height):
            if previousGen[x][y].getweather() == 0:
                canvas.itemconfig(cell[x][y], fill="yellow")
            elif previousGen[x][y].getweather() == 1:
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
#Original size 800 x 600
canvas = Canvas(root, width=800, height=600, highlightthickness=0, bd=0, bg='white')
canvas.pack()
put_cells()

images = []

for i in range(0, 32): #comment to make infinite
    make_frames()
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    xx = x + canvas.winfo_width()
    yy = y + canvas.winfo_height()
    images.append(ImageGrab.grab((x, y, xx, yy)))

imageio.mimsave('ac.gif', images, duration=0.5)

root.mainloop()