import numpy as np
from heun import *
from plotting import *
from save import *
from tasks import *

def main():
    #one_spin()
    #one_spin(alpha=0.05)
    task_2()


def run_simulation():
    params = EquationParameters()
    n = 1
    t_max = 10
    h = 0.01
    N = int(t_max//h)
    S = np.zeros((N, n, 3))
    S[0,:,0] = 1
    S[0,:,1] = 0
    S[0,:,2] = 0
    S[0,0,0] = 0
    S[0,0,1] = 1
    S[0,0,2] = 1
    S = heun(S, t_max, h, params)
    return S, np.linspace(0,t_max,N)

def task_2():
    n = 3
    t_max = 10
    h = 0.01
    N = int(t_max//h)
    params = EquationParameters()
    params.J = 0.5
    params.d_z = 0.1
    params.B_0 = 0.0
    params.alpha=0.05
    S = np.zeros((N, n, 3))
    # TODO: Make a random fuction to do this.
    S[0,0,0] = 0.1
    S[0,0,1] = 0.1
    S[0,0,2] = 0.8
    S[0,1,0] = 0.3
    S[0,1,1] = 0.7
    S[0,1,2] = 0
    S[0,2,0] = 0.5
    S[0,2,1] = 0.5
    S[0,2,2] = 0.5
    #spin_chain(S, params, t_max,  h)
    #plot_results(S, z=True)
    #phase_plot(S, 0, 2)
    #phase_plot(S, 0, 1)
    #phase_plot(S, 1, 2)

    params = EquationParameters()
    params.J = 0.5
    params.d_z = 0.1
    S = np.zeros((N, n, 3))
    S[0,:,0] = 0
    S[0,:,1] = 0
    S[0,:,2] = 1
    S[0,0,0] = 0
    S[0,0,1] = 0.1
    S[0,0,2] = 0.9
    spin_chain(S, params, t_max, h, anim=True)
    plot_results(S, x=True)
    phase_plot(S, 0, 1)







#S, t = run_simulation()
#save_data("../report/data/S.csv", S, t)
#plot_results(S)

main()
#plot_3d(S)
