import numpy as np
import matplotlib.pyplot as plt

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
    phi = phi_0 - 4.55*omega_0*time # For RK4, use 9.0 instead.
    print(phi.shape)
    sol = np.zeros((len(time), 3))
    sol[:,0] = np.sin(theta_0)*np.cos(phi[:])
    sol[:,1] = np.sin(theta_0)*np.sin(phi[:])
    sol[:,2] = np.full(len(time), np.cos(theta_0))
    return sol


def plot_analytical(S, params, time):
    analytical = analytical_solution(S[0,0,:], params, time)
    plt.plot(time, analytical[:,0], label="Analytical")

def get_error(S, an_sol):
    """ Returns difference between computed and analytical solution. 
        This function should be called on solutions for several
        values of the time step length h.
        Arguments:  
            S:      Spin array containing one particle
                    and several time steps, i.e. S[:,0,:].
            an_sol: Spin array, containing the analytical solution
                    for one particle.
        Returns:
            error:  Float.
    """
    # The phase plot is a circle/spiral in the analytical/numerical
    # case (respectively). Therefore, compute the radius of the
    # position in the xy plane, and compare to get the error.
    r_an = np.sqrt(an_sol[:,0]**2 + an_sol[:,1]**2) # This should be constant
    r_comp = np.sqrt(S[:,0]**2 + S[:,1]**2) # This will change with time.
    # Both S and an_sol are computed for the same time values.
    # Therefore, the error can be calculated using the 2-norm.
    # More generally, np.piecewice could be used. 
    # This would allow for fewer calls to analytical_solution().
    error_r = np.linalg.norm(r_an - r_comp)/np.linalg.norm(r_an)
    return error_r

