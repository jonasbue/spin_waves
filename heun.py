import numpy as np
import matplotlib.pyplot as plt
# Maybe add scipy sparse at some point?
# After first implementation, that doesn't
# strike me as particularly practical.

class EquationParameters:
    """ A class containing the parameters of the equation of motion."""
    J       = 1.0   # Coupling constant between neighboring spins.
                    # Would be nice to genaralize this to a function
                    # to allow for long distance coupling, 
                    # but that is really unnecessary for now.
    d_z     = 0.0   # Anisometry constant.
    mu      = 1.0   # Magnetic moment. 
                    # Not sure if we're taking this to be constant
                    # or summing over all S's to find it.
    gamma   = 1.0   # Gyromagnetic ratio.
    alpha   = 0.0   # Damping constant.
    B       = np.array([0,0,1.0])   # External magnetiic field.
    ksi     = np.array([0,0,0])     # Thermal noise.
                                    # Will probably stay zero.

def heun(S, t_max, h, params, normalize=True):
    """ Solves a differential equation using Heun's method.
        Arguments:
            n:          int. The number of spins (particles).
            t_max:      float. The duration of the simulation.
            h:          float. The size of the time steps.
            params:     EquationParameters. Class containing 
                        all parameters required by the time_step()
                        function.
            normalize:  bool. If true, S is normalized to length 1
                        after every time step.
        Returns:
        S:      Array (1D). The spins of all particles.
    """
    N = len(S)
    # Assert that all Sj have a nonzero spin.
    assert np.any(np.linalg.norm(S[0,:,:], axis=1) == 0) == False
    for i in range(N-1):
        # First, normalize S[i] so that the length of S is conserved.
        if normalize:
            S_abs = np.linalg.norm(S[i,:,:], axis=1)
            S[i,:,:] = np.divide(S[i,:], np.transpose(np.tile(S_abs, (3,1))))
        S[i+1,:,:] = heun_step(S[i,:,:], h, params)
    return S

def heun_step(S, h, params):
    S_p = S + h*time_step(S, params)
    S_new = S + 0.5*h*(S_p + time_step(S_p, params))
    return S_new

def time_step(S, params):
    C = params.gamma / (params.mu * (1 + params.alpha**2))
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

    return C * Sj_cross_H + params.alpha * np.cross(S[:,:], Sj_cross_H)
