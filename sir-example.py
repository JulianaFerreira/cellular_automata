import matplotlib.pylab as plt

N = 1000000
S = N - 1
I = 1
R = 0
beta = 0.5 # infection rate
mu = 0.1 # recovery rate

sus = [] # susceptible compartment
inf = [] # infected compartment
rec = [] # recovered compartment

def infection(S, I, R, N):
    for t in range (1, 100):
        S = S -(beta * S * I)/N
        I = I + ((beta * S * I)/N) - R
        R = mu * I

        sus.append(S)
        inf.append(I)
        rec.append(R)

infection(S, I, R, N)

figure = plt.figure()
figure.canvas.set_window_title('Compartimental model')

inf_line, = plt.plot(inf, label='I(t)')

sus_line, = plt.plot(sus, label='S(t)')

rec_line, = plt.plot(rec, label='R(t)')
plt.legend(handles=[inf_line, sus_line, rec_line])

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

plt.xlabel('T')
plt.ylabel('N')


plt.show()