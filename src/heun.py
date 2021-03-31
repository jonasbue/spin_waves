import numpy as np
import matplotlib.pyplot as plt
import time

class EquationParameters:
    """ A class containing the parameters of the equation of motion."""
    J       = 0.0   # Coupling constant between neighboring spins.
                    # Would be nice to genaralize this to a function
                    # to allow for long distance coupling, 
                    # but that is really unnecessary for now.
    d_z     = 0.0   # Anisometry constant.
    mu      = 1.0   # Magnetic moment. 
                    # Not sure if we're taking this to be constant
                    # or summing over all S's to find it.
    gamma   = 1.0   # Gyromagnetic ratio.
    alpha   = 0.0   # Damping constant.
    B_0     = 1.0
    B       = np.array([0,0,B_0])   # External magnetiic field.
    ksi     = np.array([0,0,0])     # Thermal noise.
                                    # Will probably stay zero.

def integrate(S, t_max, h, params, method):
    """ Solves a differential equation using Heun's method.
        Arguments:
            n:          int. The number of spins (particles).
            t_max:      float. The duration of the simulation.
            h:          float. The size of the time steps.
            params:     EquationParameters. Class containing 
                        all parameters required by the time_step()
                        function.
            method:     Function. The Runge-Kutta method to be used.
                        Defaults ho heun(), which is required
                        by the project description.
        Returns:
        S:      Array (1D). The spins of all particles.
    """
    N = len(S)
    # Assert that all Sj have a nonzero spin.
    assert np.any(np.linalg.norm(S[0,:,:], axis=1) == 0) == False
    print("Running simulation using", method.__name__[:-5] 
    + f"'s method, with h = {h}.")

    start_time = time.time()
    for i in range(N-1):
        status_bar(i, N)
        # First, normalize S[i] so that the length of S is conserved.
        # Doing this at every instance feels wrong,
        # but it prevents divergence and the results look as expected.
        # If I normalize only at t=0, the the length diverges horribly
        # for large t.
        # TODO: Discuss with someone.
        S_abs = np.linalg.norm(S[i,:,:], axis=1)
        S[i,:,:] = np.divide(S[i,:], np.transpose(np.tile(S_abs, (3,1))))
        S[i+1,:,:] = method(S[i,:,:], h, params)
    finish_time = time.time()
    print(" Done in", finish_time - start_time, "seconds.")
    return S

def heun_step(S, h, params):
    """ Iterates one step of the Heun method.
        Arguments:
            S:      Spin array for one point in time (such as S[i,:,:]).
            h:      Step length in time.
            params: EquationParameters.
        Return:
            S_new:  The next iteration of the spin array.
    """
    # There is no explicit time dependence in the equation on motion.
    # Therefore, only S and params are needed in time_step, not h.
    dS = time_step(S, params)
    S_p = S + h*dS
    S_new = S + 0.5*h*(dS + time_step(S_p, params))
    return S_new

def euler_step(S, h, params):
    """ Integrates using Euler's method."""
    S_new = S + h*time_step(S, params)
    return S_new

def rk4_step(S, h, params):
    """ Integrate using the classical Runge-Kutta method. """
    # All the function calls could make this less efficinent
    # than the lower order methods, 
    # because potentially long arrays are used.
    k1 = time_step(S, params)
    k2 = time_step(S + 0.5*h*k1, params)
    k3 = time_step(S + 0.5*h*k2, params)
    k4 = time_step(S + h*k3, params)
    S_new = S + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    return S_new


def time_step(S, params):
    """ Calculates a time step of the Heun method.
        This function is specific for one particular equation of motion.
        Arguments:
            S:      Spin array for one point in time.
            h:      Step length in time.
            params: EquationParameters. Hold parameters for the
                    equation of mortion.
        Returns:
            dtS:    The time derivative of S.
        
    """
    C = -params.gamma / (params.mu * (1 + params.alpha**2))
    Sj_cross_H = np.zeros(S.shape)
    Sz = np.transpose(np.tile(S[:,2], (3,1)))

    # This is the "main body" of the equation of motion,
    # containing everythin but the correlation 
    # between different spins/particles.
    Sj_cross_H = (2*Sz[:,:]*np.cross(S[:,:], np.tile([0,0,1], (len(S),1)))
        + params.mu*np.cross(S[:,:], np.tile(params.B, (len(S), 1)))
        - np.cross(S[:,:], params.ksi))
    # Next we add a correlation term.
    # The end points only depend on one other point, so we handle
    # the correlation term separately for those.
    # If n = 1 or J = 0, then there is not correlation. 
    if len(S) > 1:
        Sj_cross_H[0] += 2*params.J*np.cross(S[0,:], S[1,:])
        Sj_cross_H[-1] += 2*params.J*np.cross(S[-1,:], S[-2,:])
        # Lastly, we add de correlation term for the remaining points.
        if len(S) >= 3:
            Sj_cross_H[1:-1] += 2*params.J*(np.cross(S[1:-1,:], S[0:-2,:] + S[2:,:]))

    return C * (Sj_cross_H + params.alpha * np.cross(S[:,:], Sj_cross_H))

def status_bar(i, N):
    l = 30
    progress = l*i//N
    print("\r[" + "="*progress + ">" + " "*(l-progress) + "]", end="")
