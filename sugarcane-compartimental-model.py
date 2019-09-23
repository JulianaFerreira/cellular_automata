import matplotlib.pylab as plt

N = 1000000
S = N - 1
I = 1
R = 0
beta = 0.5 # infection rate
mu = 0.1 # recovery rate

good = [] # good compartment
med = [] # medium compartment
bad = [] # bad compartment

def infection(S, I, R, N):
    for t in range (1, 100):
        G = S -(beta * S * I)/N
        M = I + ((beta * S * I)/N) - R
        B = mu * I

        good.append(G)
        med.append(M)
        bad.append(B)

infection(S, I, R, N)

figure = plt.figure()
figure.canvas.set_window_title('Compartimental model')

good_line, = plt.plot(good, label='Good(t)')

med_line, = plt.plot(med, label='Medium(t)')

bad_line, = plt.plot(bad, label='Bad(t)')
plt.legend(handles=[med_line, good_line, bad_line])

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.xlabel('T')
plt.ylabel('N')


plt.show()