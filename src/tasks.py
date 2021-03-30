from heun import *
from simulation import *

def task_1():
    params = EquationParameters()
    # First, look at one spin.
    ##S = run_simulation(1, params, first_particle=np.array([0,0.1,0.9]))
    # Second, perform an error analysis.
    # Third, include damping.
    params.alpha = 0.0
    params.d_z = 0.0
    S_init = np.array([0,0.1,0.9])
    #for method in [heun_step, euler_step, rk4_step]:
    #    S = run_simulation(
    #        1, params, t_max=30, h=0.01,
    #        first_particle=S_init, 
    #        plot=True,
    #        save=True,
    #        method=method)
    methods = [heun_step, euler_step, rk4_step]
    N_arr = np.array([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    errors = np.zeros((len(methods), len(N_arr)))
    for (i, method) in enumerate(methods):
        errors[i] = convergence_plot(S_init, params, method, N_arr)
    save_errors("../report/data/errors.csv", errors, N_arr, methods)
    plt.show()

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

