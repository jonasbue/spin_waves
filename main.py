import numpy as np
from heun import *


def run_simulation():
    params = EquationParameters()
    n = 1
    t_max = 20
    h = 0.01
    N = t_max//h
    N = int(t_max//h)
    S = np.zeros((N, n, 3))
    #S[0,:,0] = 0
    #S[0,:,1] = 0
    #S[0,:,2] = 1
    S[0,0,0] = 0
    S[0,0,1] = 1
    S[0,0,2] = 1
    S = heun(S, t_max, h, params)
    return S


def plot_results(S):
    N = len(S)
    plt.plot(np.arange(N), S[:,:,0], label="x")
    plt.plot(np.arange(N), S[:,:,1], label="y")
    plt.plot(np.arange(N), S[:,:,2], label="z")
    plt.legend()
    plt.show()

S = run_simulation()
plot_results(S)

