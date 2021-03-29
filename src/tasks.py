from heun import *
from plotting import *

def one_spin(alpha=0.0, plot=True, anim=False, save=False):
    """ Task 1. Modelling a single particle spin
        in a homogeneous B-field in the z-direction.
        Returns:
            S: Spin array.
            t: Time array.
    """
    # Default parameters is mostly everything zero.
    params = EquationParameters()
    params.alpha = alpha
    n = 1
    t_max = 20
    h = 0.01
    N = int(t_max//h)
    S = np.zeros((N, n, 3))
    # Align the particle in the z-direction,
    # and then tilt it slightly along y.
    # Note: The length is normalized to one
    # in the simulation function.
    S[0,:,0] = 0
    S[0,:,1] = 0.1
    S[0,:,2] = 0.9
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

def spin_chain(S, params, t_max, h, anim=False, save=False):
    N = int(t_max//h)
    S = heun(S, t_max, h, params)
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
    return 0 # That's a nice error.
