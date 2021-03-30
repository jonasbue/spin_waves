import numpy as np
import mayavi.mlab as mlab
import matplotlib.pyplot as plt
from analysis import *
from simulation import *

def plot_3d(S):
    """ Plots a 3d chain of spins, and animates the time development.
        Argument:
            S: Array. As defined in heun.py.
    """
    n = len(S[:,0,0])
    u = S[:,:,0]
    v = S[:,:,1]
    w = S[:,:,2]

    fig = mlab.quiver3d(u[0], v[0], w[0], scale_factor=1)
    @mlab.animate(delay=100)
    def anim():
        for i in range(n):
            fig.mlab_source.set(u=u[i], v=v[i], w=w[i])
            yield
    anim()
    mlab.show()

def plot_results(S, t_max, x=False, y=False, z=False):
    """ Plots the spin directions as functions of time.
        Arguments:
            S: Array. As defined in heun.py.
    """
    N = len(S)
    time = np.linspace(0,t_max,N)
    if x:
        plt.plot(time, S[:,:,0], label="x")
    if y:
        plt.plot(time, S[:,:,1], label="y")
    if z:
        plt.plot(time, S[:,:,2], label="z")
    plt.legend()
    plt.title("Spin amplitude")
    plt.xlabel("Time")

def phase_plot(S, x, y):
    """ Makes a phase plot, i.e. a plot of the spin in one direction
        agains the spin in another direction.
        Arguments:
            S:  Spin array.
            x:  Index of the compnent to be plotted along x-axis.
                0 means x component, 1 means y and 2 means z.
            y:  Index of the compnent to be plotted along y-axis.
    """
    N = len(S)
    plt.plot(S[:,:,x], S[:,:,y], label="Spin")
    plt.legend()
    plt.title("Phase plot")
