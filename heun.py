import numpy as np
import matplotlib.pyplot as plt
# Maybe add scipy sparse at some point?

class EquationParameters:
    J       = 0.0   # Coupling constant between neighboring spins.
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
    ksi     = np.array([0,0,0])     # Thermal noise.
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
    print("Initial:")
    print(S)
    for i in range(N-1):
        S[i+1,:,:] = heun_step(S[i,:,:], h, params)
    return S

def heun_step(S, h, params):
    S_p = S + h*time_step(S, params)
    S_new = S + 0.5*h*(S_p + time_step(S_p, params))
    return S_new

def time_step(S, params):
    C = params.gamma / (params.mu * (1 + params.alpha**2))
    Sj_cross_H = (
        2*params.J*np.cross(S[:,:], S[:,1:] + S[:,:-1])
        + 2*S[:,2]*np.cross(S[:,:], np.array([0,0,1]))
        + params.mu*np.cross(S[:,:], params.B)
        - np.cross(S[:,:], params.ksi))
    return C * Sj_cross_H + params.alpha * np.cross(S[:,:], Sj_cross_H)

params = EquationParameters()

t_max = 5
h = 0.01
N = t_max//h
S = heun(1, t_max, h, params)
plt.plot(np.arange(N), S[:,:,0], label="x")
plt.plot(np.arange(N), S[:,:,1], label="y")
plt.plot(np.arange(N), S[:,:,2], label="z")
plt.legend()
plt.show()

print("Final:")
print(S)


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
