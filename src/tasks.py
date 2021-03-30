from heun import *
from simulation import *

def task_1():
    params = EquationParameters()
    params.alpha = 0.0
    params.d_z = 0.0
    S_init = np.array([0,0.1,0.9])
    # First, look at one spin.
    #one_tilted(params)

    # Second, perform an error analysis.
    # Do not run this. It takes half an hour.
    #one_tilted_error(params, S_init)

    # Third, include damping.
    #one_tilted_damping(params)


def task_2():
    n = 3
    t_max = 10
    h = 0.01
    N = int(t_max//h)
    params = EquationParameters()

    # First, the ground state.
    params.J = 0.5
    params.d_z = 0.1
    params.B_0 = 0.0
    params.alpha=0.05
    S = np.zeros((N, n, 3))
    S = run_simulation(n, params, init="random")

    # Second, mangnons.
    params = EquationParameters()
    params.J = 0.5
    params.d_z = 0.1
    S = run_simulation(n, params, init="random")


def one_tilted(params):
    for method in [heun_step, euler_step, rk4_step][0]:
        S = run_simulation(
            1, params, t_max=30, h=0.01,
            first_particle=S_init, 
            plot=True,
            save=True,
            method=method)


def one_tilted_error(params, S_init):
    methods = [euler_step, heun_step, rk4_step]
    #N_arr = np.array([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    h_arr = np.array([0.1, 0.01, 0.001, 0.0001, 0.00001])
    errors = np.zeros((len(methods), len(h_arr)))
    for (i, method) in enumerate(methods):
        errors[i] = convergence_plot(S_init, params, method, h_arr)
    save_errors("../report/data/new_errors.csv", errors, h_arr, methods)
    plt.show()

def one_tilted_damping(params):
    params.alpha=0.05
    S = run_simulation(
        1, params, t_max=30, h=0.01,
        first_particle=S_init, 
        plot=True,
        save=True,
        method=heun_step)

