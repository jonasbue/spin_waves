import numpy as np

def save_data(filename, S, time, analytical=[]):
    """ Saves a table of spins on the following format:
        t   x0  y0  z0  x1  y1  z1  ...
        0   0   0   1   0   0   1   ...
        h   0   0   1   0   0   1   ...
                    ....
        Arguments:
            filename: String.
            S: Array. As defined in heun.py.
    """
    t = S.shape[0] # Number of time steps.
    n = S.shape[1] # Number of particles.
    N = np.zeros(t)
    N[:n] = np.arange(n)
    assert len(time) == t

    # Flatten S along innermost axis, to make it 2d.
    S_save = S.reshape((t,3*n))
    S_save = np.column_stack((time, S_save))

    headers = "t\t" + "\t".join(f"x{i}\ty{i}\tz{i}" for i in range(n))
    if len(analytical) != 0:
        S_save = np.column_stack((S_save, analytical))
        headers += "".join(f"\tanalytical_x{0}\tanalytical_y{0}\tanalytical_z{0}" for i in range(n))
    np.savetxt(filename, S_save, header=headers, comments="", delimiter="\t")
    print(f"Data saved to {filename} successfully.")

