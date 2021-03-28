import numpy as np
import mayavi.mlab as mlab
import matplotlib.pyplot as plt

def plot_3d(S):
    n = len(S[:,0,0])
    #x = np.zeros(n)
    #y = np.zeros(n)
    #z = np.zeros(n)
    u = S[:,:,0]
    v = S[:,:,1]
    w = S[:,:,2]
    #xu = np.array(np.meshgrid(x,u))
    #yv = np.array(np.meshgrid(y,v))
    #zw = np.array(np.meshgrid(z,w))
    #print(xu[1].shape)
    #print(yv.shape)
    #print(zw.shape)
    fig = mlab.quiver3d(u[0], v[0], w[0], scale_factor=1)

    @mlab.animate(delay=100)
    def anim():
        for i in range(n):
            fig.mlab_source.set(u=u[i], v=v[i], w=w[i])
            yield
    anim()
    mlab.show()

def plot_results(S):
    N = len(S)
    plt.plot(np.arange(N), S[:,:,0], label="x")
    plt.plot(np.arange(N), S[:,:,1], label="y")
    plt.plot(np.arange(N), S[:,:,2], label="z")
    plt.legend()
    plt.show()

