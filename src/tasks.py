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
    # TODO: Run this again. I found a mistake..
    #one_tilted_error(params, S_init)
    # Third, include damping.
    # TODO: Implement curve fitting here.
    one_tilted_damping(S_init, params)


def task_2():
    n = 10
    t_max = 50
    h = 0.01
    N = int(t_max//h)
    params = EquationParameters()
    # First, the ground state.
    J = 0.5
    # Positive J
    #print("Chain, ground state")
    #chain_ground_state(n, params, J)
    # Negative J
    #chain_ground_state(n, params, -J)
    # Second, mangnons.
    print("Chain, magnons.")
    t_max = 30
    save=True
    anim=False
    magnons(n, params, J, t_max, save, anim)


def one_tilted(params):
    for method in [heun_step, euler_step, rk4_step][0]:
        S = run_simulation(
            1, params, t_max=40, h=0.01,
            first_particle=S_init, 
            plot=True,
            save=True,
            anim=False,
            analytical=False,
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

def one_tilted_damping(S_init, params):
    params.alpha=0.05
    params.d_z=0.5
    S = run_simulation(
        1, params, t_max=30, h=0.01,
        first_particle=S_init, 
        plot=True,
        save=True,
        anim=False,
        analytical=False,
        method=heun_step)
    

def chain_ground_state(n, params, J):
    params.d_z = 0.1
    params.B_0 = 0.0
    params.alpha = 0.05
    params.J = J
    S = run_simulation(n, params, heun_step, t_max=30, anim=True, init="random")


def magnons(n, params, J, t_max, save, anim):
    params.J = 0.0
    params.d_z = 0.1
    # Tilt all, watch for precession.
    #print("Tilt all, watch for precession. No correlation.")
    S = run_simulation(n, params, heun_step, save=save, anim=anim, init="z_tilt")
    # All particles start along z, except for the first one, which is tilted.
    # J = 0, so only the first should rotate.
    # This is a test, and will not be plotted in the report. Right?
    print("One tilted, watch for precession. No correlation.")
    S = run_simulation(n, params, heun_step, t_max=t_max, save=False, anim=anim, init="z",
        first_particle=np.array([0,0.1,0.9]))

    # Now, set J > 0
    params.J = J
    # First particle is tilted, all others along z.
    # This is a test, and will not be plotted in the report. Right?
    print("One tilted, with correlation.")
    S = run_simulation(n, params, heun_step, t_max=t_max, save=False, anim=anim, init="z",
        first_particle=np.array([0,1,1]))

    # Now, set alpha > 0
    params.alpha = 0.05
    # This is the spin current, and should be included in the report.
    print("One tilted, with damping and correlation.")
    S = run_simulation(n, params, heun_step, t_max=t_max, save=save, anim=anim, init="z",
        first_particle=np.array([0,1,1]), savename="magnon_random")

    # Now, set J < 0.
    params.J = -J
    params.alpha = 0.05
    # Random, all tilted and one tilted are of interest here.
    print("Random directions, with damping and negative correlation.")
    S = run_simulation(n, params, heun_step, t_max=t_max, save=save, anim=anim, init="random", savename="magnon_random")
    print("All tilted, with damping and negative correlation.")
    S = run_simulation(n, params, heun_step, t_max=t_max, save=save, anim=anim, init="z_tilt", savename="magnon_all_tilted")
    print("One tilted, with damping and negative correlation.")
    S = run_simulation(n, params, heun_step, t_max=t_max, save=save, anim=anim, init="z",
        first_particle=np.array([0,1,1]), savename="magnon_one_tilted")

    # Lastly, look at the magnetization.
    # TODO: Make a function that calculates magnetization of the system.
    # Do random first, find the magnetization in equillibrium.
    params.alpha = 0.05
    #S = run_simulation(n, params, heun_step, save=False, anim=True, init="random")

