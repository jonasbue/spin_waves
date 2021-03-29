from heun import *
from plotting import *

def one_spin(S, params, t_max, h, plot=True, anim=False, save=False):
    """ Task 1. Modelling a single particle spin
        in a homogeneous B-field in the z-direction.
        Arguments:
            S: Array. Spin array, containing the initial conditions.
        Returns:
            S: Spin array.
            t: Time array.
    """
    N = len(S)
    S = heun(S, t_max, h, params)
    t = np.linspace(0,t_max,N)
    if plot:
        plot_results(S, x=True, y=True, z=True)
        phase_plot(S, 0, 1)
    if anim:
        plot_3d(S)
    if save:
        # To avoid periods in file name, use a dash instead.
        a_str = str(alpha).replace(".", "-")
        filename = f"../report/data/one_spin_alpha_{a_str}.csv"
        save_data(filename, S, t)
    return S, np.linspace(0,t_max,N)


def spin_chain(S, params, t_max, h, plot=True, anim=False, save=False):
    N = int(t_max//h)
    S = heun(S, t_max, h, params)
    if plot:
        plot_results(S, z=True)
        phase_plot(S, 0, 2)
    if anim:
        plot_3d(S)
    if save:
        # To avoid periods in file name, use a dash instead.
        a_str = str(params.alpha).replace(".", "-")
        filename = f"../report/data/{n}_spins_alpha_{a_str}.csv"
        save_data(filename, S, t)
    return S, np.linspace(0,t_max,N)
    

def error_analysis():
    #TODO: Make this.
    return 0 # Zero is a nice error.


def run_simulation(n, params, t_max=10, h=0.01, init="x", 
    first_particle=np.array([]), plot=True, anim=False, save=False):
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
        one_spin(S, params, t_max, h,
            plot=plot, anim=anim, save=save)
    elif n > 1:
        spin_chain(S, params, t_max, h,
            plot=plot, anim=anim, save=save)
    S = heun(S, t_max, h, params)
    return S


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
        # Note: The length is normalized to one
        # in the simulation function.
        S[0,:,0] = 0
        S[0,:,1] = 0.1
        S[0,:,2] = 1
    elif init == "random":
        # Quality random numbers.
        S[0,0,0] = 0.1
        S[0,0,1] = 0.1
        S[0,0,2] = 0.8
        S[0,1,0] = 0.3
        S[0,1,1] = 0.7
        S[0,1,2] = 0
        S[0,2,0] = 0.5
        S[0,2,1] = 0.5
        S[0,2,2] = 0.5
    # Now change the first particle.
    if first_particle.size:
        S[0,0,:] = first_particle
    return S

