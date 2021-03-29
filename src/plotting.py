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


def analytical_solution(init, params, time):
    """ Returns the analytical solution of a system with one single particle.
        Arguemnts:
            init:   Array. Initial condition of the particle.
                    Init for particle i is obtained using S[0,i,:].
            params: EquationParameters. Parameters of the equation of motion.
            t:      Float. Time of evaluation. Could possibly be an array.
        Returns:
            S:      An array containing the cartesian coodrinates
                    of the analytical solution.
    """
    x, y, z = init
    phi_0 = np.arctan(y/x)
    theta_0 = np.arccos(z/np.linalg.norm(init))
    omega_0 = ((params.gamma/params.mu) * (2*np.cos(theta_0) 
            + params.mu*params.B_0) *np.sin(theta_0))

    print(time.shape)
    # The 4.55 is set by hand (ad hoc) here.
    # The amplitude is the important part.
    phi = phi_0 - 4.55*omega_0*time
    print(phi.shape)
    sol = np.zeros((len(time), 3))
    sol[:,0] = np.sin(theta_0)*np.cos(phi[:])
    sol[:,1] = np.sin(theta_0)*np.sin(phi[:])
    sol[:,2] = np.full(len(time), np.cos(theta_0))
    return sol


def plot_analytical(S, params, time):
    analytical = analytical_solution(S[0,0,:], params, time)
    plt.plot(time, analytical[:,0], label="Analytical")

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
