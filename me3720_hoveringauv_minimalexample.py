import holoocean
import numpy as np
from pynput import keyboard
import matplotlib.pyplot as plt

scenario = {
    "name": "test_rgb_camera",
    "world": "SimpleUnderwater",
    "package_name": "Ocean",
    "main_agent": "auv0",
    "ticks_per_sec": 10,
    "agents": [
        {
            "agent_name": "auv0",
            "agent_type": "HoveringAUV",
            "sensors": [
                {
                    "sensor_type": "RGBCamera",
                    "socket": "CameraSocket",
                    "configuration": {
                        "CaptureWidth": 512,
                        "CaptureHeight": 512
                    }
                },
                {
                    "sensor_type": "DynamicsSensor",
                    # "configuration":{
                    #     "UseRPY": False # Use quaternion
                    # }
                },
            ],
            "control_scheme": 0,
            "location": [0, 0, -10]
        }
    ]
}


pressed_keys = list()
force = 25

def on_press(key):
    global pressed_keys
    if hasattr(key, 'char'):
        pressed_keys.append(key.char)
        pressed_keys = list(set(pressed_keys))

def on_release(key):
    global pressed_keys
    if hasattr(key, 'char'):
        pressed_keys.remove(key.char)

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

def parse_keys(keys, val):
    command = np.zeros(8)
    if 'i' in keys:
        command[0:4] += val
    if 'k' in keys:
        command[0:4] -= val
    if 'j' in keys:
        command[[4,7]] += val
        command[[5,6]] -= val
    if 'l' in keys:
        command[[4,7]] -= val
        command[[5,6]] += val

    if 'w' in keys:
        command[4:8] += val
    if 's' in keys:
        command[4:8] -= val
    if 'a' in keys:
        command[[4,6]] += val
        command[[5,7]] -= val
    if 'd' in keys:
        command[[4,6]] -= val
        command[[5,7]] += val

    return command


def get_states_6dof(dynamics_sensor_output_rpy):
    x = dynamics_sensor_output_rpy
    a = x[:3]
    v = x[3:6]
    p = x[6:9]
    alpha = x[9:12]
    omega = x[12:15]
    theta = x[15:18]
    # state_6dof = np.concatenate((p,theta))
    pos = np.concatenate((p,theta))
    vel = np.concatenate((v,omega))
    acc = np.concatenate((a,alpha))
    state_6dof = dict(pose=pos, velocity=vel,acceleration=acc)
    return state_6dof

plt.ion()
x_data = []
y_data = []
''
fig, ax = plt.subplots()
line, = ax.plot(x_data, y_data)

ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_title("Real-time Plot")

with holoocean.make(scenario_cfg=scenario) as env:
    while True:
        if 'q' in pressed_keys:
            break
        command = parse_keys(pressed_keys, force)
        # print(command)

        #send to holoocean
        env.act("auv0", command)
        simul_state = env.tick()
        auv_state = get_states_6dof(simul_state["DynamicsSensor"])
        state = auv_state["pose"]
        print(state)

        x_data.append(state[0])
        y_data.append(state[1])

        line.set_xdata(x_data)
        line.set_ydata(y_data)

        ax.relim()
        ax.autoscale_view()

        fig.canvas.draw()
        fig.canvas.flush_events()





