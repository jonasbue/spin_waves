import numpy as np
import mayavi.mlab as mlab
import matplotlib.pyplot as plt

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

def plot_results(S):
    """ Plots the spin directions as functions of time.
        Arguments:
            S: Array. As defined in heun.py.
    """
    N = len(S)
    plt.plot(np.arange(N), S[:,:,0], label="x")
    plt.plot(np.arange(N), S[:,:,1], label="y")
    plt.plot(np.arange(N), S[:,:,2], label="z")
    plt.legend()
    plt.show()

