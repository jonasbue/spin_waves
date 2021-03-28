import numpy as np
from heun import *
from plotting import *
from save import *


def run_simulation():
    params = EquationParameters()
    n = 10
    t_max = 200
    h = 0.1
    N = t_max//h
    N = int(t_max//h)
    S = np.zeros((N, n, 3))
    S[0,:,0] = 1
    S[0,:,1] = 0
    S[0,:,2] = 0
    S[0,0,0] = 0
    S[0,0,1] = 0
    S[0,0,2] = 1
    S = heun(S, t_max, h, params)
    return S, np.linspace(0,t_max,N)

S, t = run_simulation()
save_data("./report/data/S.csv", S, t)
#plot_results(S)

plot_3d(S)
