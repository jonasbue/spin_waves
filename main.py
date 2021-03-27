import numpy as np
from heun import *

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


