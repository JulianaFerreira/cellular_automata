import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import random
import copy
from tkinter import *

# Total population, N.
N = 4800
# Initial number of infected and recovered individuals, I0 and R0.
I0, R0 = 1, 0
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - R0
# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
beta, gamma = 0.3, 0.1
# A grid of time points (in days)
time = 100
t = np.linspace(0, time, time)

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# Initial conditions vector
y0 = S0, I0, R0
# Integrate the SIR equations over the time grid, t.
ret = odeint(deriv, y0, t, args=(N, beta, gamma))
S, I, R = ret.T

# Plot the data on three separate curves for S(t), I(t) and R(t)
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, axisbelow=True)
ax.plot(t, S/N, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I/N, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R/N, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
ax.set_xlabel('Time /days')
ax.set_ylabel('Number (4800s)')
ax.set_ylim(0,1.2)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.savefig('myplot.png')
plt.show()



#------------AUTOMATO---------------
class Cell:

    def __init__(self, time, state):
        self.time = time
        self.state = state

    def gettime(self):
        return self.time

    def settime(self, time):
        self.time = time

    def getstate(self):
        return self.state

    def setstate(self, state):
        self.state = state


cell = [[0 for row in range(-1, 61)] for col in range(-1, 81)]
firstGen = [[0 for row in range(-1, 61)] for col in range(-1, 81)]
temporary = [[0 for row in range(-1, 61)] for col in range(-1, 81)]


def make_frames():
    processing()
    paint_cells()
    root.after(1000, make_frames)


def put_cells():
    # state: 0 = s, 1 = i, 2 = r
    aleatory_cells = [Cell(0, 0), Cell(0, 0), Cell(0, 0), Cell(0, 0), Cell(0, 0),
                      Cell(0, 0), Cell(0, 0), Cell(0, 0), Cell(0, 0), Cell(0, 0),
                      Cell(0, 0), Cell(0, 1), Cell(0, 0), Cell(0, 0), Cell(0, 0),
                      Cell(0, 0), Cell(0, 0), Cell(0, 0), Cell(0, 0), Cell(0, 0)]

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
            aleatory_cells = [Cell(0, 0), Cell(0, 0), Cell(0, 0), Cell(0, 0), Cell(0, 0),
                              Cell(0, 0), Cell(0, 0), Cell(0, 0), Cell(0, 0), Cell(0, 0),
                              Cell(0, 0), Cell(0, 1), Cell(0, 0), Cell(0, 0), Cell(0, 0),
                              Cell(0, 0), Cell(0, 0), Cell(0, 0), Cell(0, 0), Cell(0, 0)]

            if firstGen[x][y].getstate() == 0:
                cells_state_0 += 1
            elif firstGen[x][y].getstate() == 1:
                cells_state_1 += 1
            elif firstGen[x][y].getstate() == 2:
                cells_state_2 += 1

            temporary[x][y] = copy.copy(firstGen[x][y])
            temporary[x][y].setstate(
                getNewState2D(firstGen[x][y].getstate(), infected_neighbors_state1, infected_neighbors_state2))
            temporary[x][y].settime(temporary[x][y].gettime() + 1)


    archive = open("ac.txt", "a")
    archive2 = open("ac.txt", "r")
    content = archive2.readlines()
    number_of_lines = len(content)
    archive.write("mounth: %d" % ((number_of_lines / 8) + 1) + "\n")
    archive.write("cells susceptible: %d" % cells_state_0 + "\n")
    archive.write("cells infected: %d" % cells_state_1 + "\n")
    archive.write("cells recovered: %d" % cells_state_2 + "\n")
    archive.write("----------------------------" + "\n")

    for y in range(0, 60):
        for x in range(0, 80):
            firstGen[x][y] = temporary[x][y]


def getRandomNumber(distribution):
    if distribution == 0:
        returningRandomNumber = np.random.uniform() # UNIFORM
    elif distribution == 1:
        returningRandomNumber = np.random.normal(.5, .1) # NORMAL
    elif distribution == 2:
        returningRandomNumber = (np.random.binomial(20, .5, 100) % 10) * 0.1 # BINOMIAL
    elif distribution == 3:
        returningRandomNumber = np.random.poisson(2) * .1 # POISSON
    return returningRandomNumber

''' This method calculates the new state of the cell based on Moore neighborhood '''
def getNewState2D(selfCharacter,infected_neighbors_state1,infected_neighbors_state2):
    newState = selfCharacter

    if selfCharacter == 0: # If S and there is an Infected close, be Infected
        if infected_neighbors_state1 > 1 or infected_neighbors_state2 > 1:
            betaChance = getRandomNumber(0)
            if betaChance < beta and betaChance > 0:
                newState = 1
    elif selfCharacter == 1: # if Infected, calculate the probability to be Recovered
        gammaChance = getRandomNumber(0)

        if gammaChance < gamma and gammaChance > 0:
            newState = 2

    return newState


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
                canvas.itemconfig(cell[x][y], fill="blue")
            if firstGen[x][y].getstate() == 1:
                canvas.itemconfig(cell[x][y], fill="red")
            if firstGen[x][y].getstate() == 2:
                canvas.itemconfig(cell[x][y], fill="green")


root = Tk()
canvas = Canvas(root, width=800, height=600, highlightthickness=0, bd=0, bg='white')
canvas.pack()
put_cells()

make_frames()
root.mainloop()