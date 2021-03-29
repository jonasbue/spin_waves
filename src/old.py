def H(S, J, B, d_z=0, mu=0):
    """ The Hamiltonian function.Computes the Hamiltonian,
        or the total energy of the system.
        Arguments:
            S:      Array (1D). The spins of all particles.
            J:      Function. The coupling constant.
            B:      Array (3D). The external magnetic field.
            d_z:    Float. The anisotropy constant. d_z > 0.
            mu:     Float. Total magnetic moment of system.
        Returns:
            H:      Float. Total energy of system, i.e. the Hamiltonian.
    """
    J_arr = J*kr_delta_arr(len(S))
    a = np.sum(np.einsum("jk,j,k", J_arr, S, S))
    return a


def J(coupling, j, k):
    """ A coupling function. Might be reformulated and
        then used to generalize the equation of motion."""
    return coupling*kr_delta(j,k)

def kr_delta(j,k):
    """ Kroenecker delta function."""
    # May be computed using explicit einsum().
    if j == k:
        return 1
    else:
        return 0

def kr_delta_arr(n):
    """ Returns an array-like kronecker delta."""
    return np.einsum('ij,kl->ijkl', np.eye(n,n), np.eye(n,n))

# Brief test of the above code.
S = np.array([1,1,2])
#a = np.sum(np.einsum("jk,j,k", J(1,j,k), S, S))
J_arr = 1*np.identity(len(S))
print(J_arr)
a = np.sum(np.einsum("jk,j,k", J_arr, S, S))
a = np.sum(np.einsum("jk,j,k", J_arr, S , S))
print(a)
