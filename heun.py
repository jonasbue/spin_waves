import numpy as np
import matplotlib.pyplot as plt
# Maybe add scipy sparse at some point?

class EquationParameters:
    J       = 1.0   # Coupling constant between neighboring spins.
                    # Would be nice to genaralize this to a function
                    # to allow for long distance coupling, 
                    # but that is really unnecessary for now.
    d_z     = 1.0   # Anisometry constant.
    mu      = 1.0   # Magnetic moment. 
                    # Not sure if we're taking this to be constant
                    # or summing over all S's to find it.
    gamma   = 1.0   # Gyromagnetic ratio.
    alpha   = 1.0   # Damping constant.
    B       = np.array([0,0,1.0])   # External magnetiic field.
    ksi     = np.array([1,0,0])     # Thermal noise.
                                    # Will probably stay zero.

def heun(n, t_max, h, params):
    """ Solves a differential equation using Heun's method.
        Arguments:
            n:      int. The number of spins (particles).
            t_max:  float. The duration of the simulation.
            h:      float. The size of the time steps.
            params: EquationParameters. Class containing 
                    all parameters required by the time_step()
                    function.
        Returns:
            S:      Array (1D). The spins of all particles.
    """
    N = int(t_max//h)
    S = np.zeros((N, n, 3))
    S[0,0,1] = 0.1
    #print("Initial:")
    #print(S)
    for i in range(N-1):
        S[i+1,:,:] = heun_step(S[i,:,:], h, params)
    return S

def heun_step(S, h, params):
    S_p = S + h*time_step(S, params)
    S_new = S + 0.5*h*(S_p + time_step(S_p, params))
    return S_new

def time_step(S, params):
    C = params.gamma / (params.mu * (1 + params.alpha**2))
    #print(S[1:-1].shape,"\n", S[2:].shape, "\n", S[:-2].shape)
    #print(2*params.J*np.cross(S[1:-1,:], S[1:,:] + S[:-1,:]))
    #print("S:")
    #print(S)

    #print("S[1:-1]\n", S[1:-1,:],"\n S[0:-2]", S[0:-2,:], "\n S[2:]", S[2:,:])
    #print(np.tile([0,0,1], (len(S)-2,1)))

    Sj_cross_H = np.zeros(S.shape)
    Sz = np.transpose(np.tile(S[:,2], (3,1)))
    print(Sz)

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

## Unnecessary stuff, right?
#def H(S, J, B, d_z=0, mu=0):
#    """ The Hamiltonian function.
#        Arguments:
#            S:      Array (1D). The spins of all particles.
#            J:      Function. The coupling constant.
#            B:      Array (3D). The external magnetic field.
#            d_z:    Float. The anisotropy constant. d_z > 0.
#            mu:     Float. Total magnetic moment of system.
#        Returns:
#            H:      Float. Total energy of system, i.e. the Hamiltonian.
#    """
#    J_arr = J*kr_delta_arr(len(S))
#    a = np.sum(np.einsum("jk,j,k", J_arr, S, S))
#    return a
#
#
#def J(coupling, j, k):
#    return coupling*kr_delta(j,k)
#
#def kr_delta(j,k):
#    """ Kroenecker delta function."""
#    # May be computed using explicit einsum().
#    if j == k:
#        return 1
#    else:
#        return 0
#
#def kr_delta_arr(n):
#    """ Returns an array-like kronecker delta."""
#    return np.einsum('ij,kl->ijkl', np.eye(n,n), np.eye(n,n))
#
#
#S = np.array([1,1,2])
##a = np.sum(np.einsum("jk,j,k", J(1,j,k), S, S))
#J_arr = 1*np.identity(len(S))
#print(J_arr)
#a = np.sum(np.einsum("jk,j,k", J_arr, S, S))
#a = np.sum(np.einsum("jk,j,k", J_arr, S , S))
#
#print(a)
############################
