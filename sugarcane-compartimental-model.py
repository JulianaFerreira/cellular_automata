import matplotlib.pylab as plt

N = 1000000
G = N - 1
M = 1
B = 0
beta = 0.5 # one state rate
mu = 0.1 # two state rate

good = [] # good compartment
med = [] # medium compartment
bad = [] # bad compartment

def infection(G, M, B, N):
    for t in range (1, 100):
        G = G -(beta * G * M)/N
        M = M + ((beta * G * M)/N) - B
        B = mu * M

        good.append(G)
        med.append(M)
        bad.append(B)

infection(G, M, B, N)

figure = plt.figure()
figure.canvas.set_window_title('Compartimental model')

good_line, = plt.plot(good, label='Good(t)')

med_line, = plt.plot(med, label='Medium(t)')

bad_line, = plt.plot(bad, label='Bad(t)')
plt.legend(handles=[good_line, med_line, bad_line])

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.xlabel('T')
plt.ylabel('N')


plt.show()