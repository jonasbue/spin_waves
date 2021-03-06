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
    ###one_tilted_error(params, S_init)
    # Third, include damping.
    # TODO: Implement curve fitting here.
    one_tilted_damping(S_init, params)


def task_2():
    n = 10
    t_max = 200
    h = 0.01
    N = int(t_max//h)
    params = EquationParameters()
    # First, the ground state.
    params.J = 1
    # Positive J
    #print("Chain, ground state")
    #chain_ground_state(n, params, J)
    # Negative J
    #chain_ground_state(n, params, -J)
    # Second, mangnons.
    print("Chain, magnons.")
    t_max = 100
    save=True
    plotting=False
    anim=True
    magnons(n, params, params.J, t_max, save, anim)

def magnetization():
    n = 10
    t_max = 50
    h = 0.01
    N = int(t_max//h)
    params = EquationParameters()
    J = 1
    params.alpha = 0.05
    t = np.linspace(0, t_max, N)

    S = run_simulation(n, params, heun_step, t_max=t_max, h=h, 
        save=False, anim=False, init="z", first_particle=np.array([0,1,1]))
    M = get_magnetization(S, params)
    data = np.column_stack((t, M))
    plt.plot(t, M)
    plt.show()
    np.savetxt("../report/magnetization_ferro.csv", data, header="t\tMz", delimiter="\t", comments="")



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
    for alpha in [0.05, 0.1, 0.2]:
        params.alpha=alpha
        params.d_z=0.5
        S = run_simulation(
            1, params, t_max=30, h=0.01,
            first_particle=S_init, 
            plot=True,
            save=True,
            anim=True,
            analytical=False,
            method=heun_step,
            savename="damping")
    

def chain_ground_state(n, params, J):
    params.d_z = 0.1
    params.B_0 = 0.0
    params.alpha = 0.05
    params.J = J
    S = run_simulation(n, params, heun_step, t_max=30, 
        periodic_bc=False, anim=True, init="random")


def magnons(n, params, J, t_max, save, anim):
    params.J = 0.0
    params.d_z = 0.1
    params.alpha = 0.0
    # Tilt all, watch for precession.
    #print("Tilt all, watch for precession. No correlation.")
    #S = run_simulation(n, params, heun_step, t_max=t_max, save=save, anim=anim, init="random",
    #    savename="random_no_coupling")
    # All particles start along z, except for the first one, which is tilted.
    # J = 0, so only the first should rotate.
    # This is a test, and will not be plotted in the report. Right?
    print("One tilted, watch for precession. No correlation.")
    #S = run_simulation(n, params, heun_step, t_max=t_max, save=save, anim=anim, init="z",
    #    first_particle=np.array([0,0.1,0.9]), savename="one_tilted_no_coupling")

    # Now, set J > 0
    params.J = J
    # First particle is tilted, all others along z.
    # This is a test, and will not be plotted in the report. Right?
    print("One tilted, with correlation.")
    S = run_simulation(n, params, heun_step, t_max=t_max, 
        periodic_bc=False, save=save, anim=anim, init="z",
        first_particle=np.array([0,1,1]), savename="magnon_ferro")

    print("One tilted, with correlation and periodic BCs.")
    #S = run_simulation(n, params, heun_step, t_max=t_max, 
    #    periodic_bc=True, save=True, anim=anim, init="z",
    #    first_particle=np.array([0,1,1]), savename="magnon_ferro_periodic")

    ## Now, set alpha > 0
    #params.alpha = 0.05
    #print("Random directions, with damping and ferromagnetic correlation.")
    #S = run_simulation(n, params, heun_step, t_max=t_max, save=save, anim=anim, 
    #    init="random", savename="random_ferro")
    ## This is the spin current, and should be included in the report.
    #print("One tilted, with damping and correlation.")
    #S = run_simulation(n, params, heun_step, t_max=t_max, save=save, anim=anim, init="z",
    #    first_particle=np.array([0,1,1]), savename="magnon_ferro")

    ## Now, set J < 0.
    #params.J = -J
    #params.alpha = 0.0
    #print("One tilted, without damping and negative correlation.")
    #S = run_simulation(n, params, heun_step, t_max=t_max, save=save, anim=anim, init="z",
    #    first_particle=np.array([0,1,1]), savename="magnon_antiferro")

    ## Set alpha > 0.
    #params.alpha = 0.05
    ## Random, all tilted and one tilted are of interest here.
    #print("Random directions, with damping and negative correlation.")
    #S = run_simulation(n, params, heun_step, t_max=t_max, save=save, anim=anim, init="random", savename="random_antiferro")
    #print("All tilted, with damping and negative correlation.")
    #S = run_simulation(n, params, heun_step, t_max=2*t_max, save=save, anim=anim, init="z_tilt", savename="magnon_all_tilted_antiferro")
    #print("One tilted, with damping and negative correlation.")
    #S = run_simulation(n, params, heun_step, t_max=2*t_max, save=save, anim=anim, init="z",
    #    first_particle=np.array([0,1,1]), savename="magnon_antiferro")

    ## Lastly, look at the magnetization.
    ## Do random first, find the magnetization in equillibrium.
    ## This is a separate function.

