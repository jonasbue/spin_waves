from heun import *
from plotting import *
from save import *
from analysis import *


def run_simulation(n, params, method, t_max=10, h=0.01, init="x", 
    first_particle=np.array([]), plot=True, 
    anim=False, save=False, analytical=True, savename=""):
    """ Runs simulation.
        Arguments:
            A lot.
        Returns:
            S: Spin array.
    """
    N = int(t_max//h) # Number of time steps
    # Initialize S
    S = make_S(init, n, N, first_particle=first_particle)
    if n == 1:
        S, time = one_spin(S, params, t_max, h, method, savename,
            plot=plot, anim=anim, save=save, analytical=analytical)
    elif n > 1:
        S, time = spin_chain(S, params, t_max, h, method, savename,
            plot=plot, anim=anim, save=save)
    return S


def one_spin(S, params, t_max, h, method, savename, plot=True, anim=False, 
    save=False, analytical=True):
    """ Task 1. Modelling a single particle spin
        in a homogeneous B-field in the z-direction.
        Arguments:
            S: Array. Spin array, containing the initial conditions.
        Returns:
            S: Spin array.
            t: Time array.
    """
    N = len(S)
    S = integrate(S, t_max, h, params, method)
    t = np.linspace(0,t_max,N)
    an_sol = analytical_solution(S[0,0,:], params, t)
    if plot:
        plot_results(S, t_max, x=True, y=True, z=True)
        if analytical:
            plt.plot(t, an_sol[:,0], linestyle="--", label="Analytical")
            plt.plot(t, an_sol[:,1], linestyle="--", label="Analytical")
            plt.plot(t, an_sol[:,2], linestyle="--", label="Analytical")
            plt.legend()
        plt.show()
        phase_plot(S, 0, 1)
        if analytical:
            plt.plot(an_sol[:,0], an_sol[:,1], linestyle="--", label="Analytical")
        plt.show()
    if anim:
        plot_3d(S)
    if save:
        # To avoid periods in file name, use a dash instead.
        a_str = str(params.alpha).replace(".", "-")
        method_name = method.__name__
        filename = f"../report/data/one_spin_{savename}_{method_name}_{N}_alpha_{a_str}.csv"
        if analytical:
            save_data(filename, S, t, an_sol)
        else:
            save_data(filename, S, t)
    return S, np.linspace(0,t_max,N)


def spin_chain(S, params, t_max, h, method, savename, plot=False, anim=False, save=False):
    N = int(t_max//h)
    S = integrate(S, t_max, h, params, method)
    time = np.linspace(0,t_max,N)
    if plot:
        plot_results(S, t_max, z=True)
        plt.show()
        phase_plot(S, 0, 2)
        plt.show()
    if anim:
        plot_3d(S)
    if save:
        # To avoid periods in file name, use a dash instead.
        a_str = str(params.alpha).replace(".", "-")
        filename = f"../report/data/{N}_spins_{savename}_alpha_{a_str}.csv"
        save_data(filename, S, time)
    return S, time
    




def make_S(init, n, N, first_particle):
    """ Creates a spin array, and gives all particles
        an initial condition based on input keyword.
        Argument:
            init:   String. The type of initial condition.
            first:  Array. Gives the initial condition
                    of the first particle in S, so that
                    this can be different than the others.
        Returns:
            S:      Spin array.
    """
    S = np.zeros((N, n, 3))
    # Assign initial conditions.
    # Note: The length is normalized to one
    # in the simulation function, so the length
    # doesn't matter here.
    if init == "z":
        S[0,:,0] = 0
        S[0,:,1] = 0
        S[0,:,2] = 1
    elif init == "x":
        S[0,:,0] = 1
        S[0,:,1] = 0
        S[0,:,2] = 0
    elif init == "z_tilt":
        # Align the particle in the z-direction,
        # and then tilt it slightly along y.
        S[0,:,0] = 0
        S[0,:,1] = 0.1
        S[0,:,2] = 1
    elif init == "random":
        # Assign random values in [-1,1) to all spin 
        # components of all particles, at time = 0.
        S[0] = 2*np.random.random_sample(S[0].shape) - 1
    # Now change the first particle.
    if first_particle.size:
        S[0,0,:] = first_particle
    return S

def convergence_plot(init, params, method, h_arr):
    """ Makes a convergence plot. """
    t_max = 10
    #all_h = np.divide(t_max, all_N)
    error = np.zeros(len(h_arr))
    for (i, h) in enumerate(h_arr):
        # Run the simulation for task 1 for all h.
        N = int(t_max//h)
        time = np.linspace(0,t_max,N)
        S = run_simulation(
            1, params, t_max=t_max, h=h,
            first_particle=np.array([0,0.1,0.9]),
            plot=False,
            method=method,
        )
        an_sol = analytical_solution(init, params, time)
        error[i] = get_error(S[:,0,:], an_sol)
    
    method_name = method.__name__[:-4]
    plt.plot(h_arr, error, marker="o", linestyle="--", label=method_name)
    plt.xscale("log")
    plt.yscale("log")
    plt.gca().invert_xaxis()
    plt.title("Convergence plot")
    plt.legend()
    return error

