import holoocean
import numpy as np

env = holoocean.make("PierHarbor-Hovering")

command = np.array([10,10,10,10,0,0,0,0])

for _ in range(1800):
    state = env.step(command)
    print(state["PoseSensor"])