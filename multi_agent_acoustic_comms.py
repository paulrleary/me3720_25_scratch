import holoocean

cfg = {
    "name": "test_acou_coms",
    "world": "SimpleUnderwater",
    "package_name": "Ocean",
    "main_agent": "auv0",
    "ticks_per_sec": 200,
    "agents": [
        {
            "agent_name": "auv0",
            "agent_type": "HoveringAUV",
            "sensors": [
                {
                    "sensor_type": "AcousticBeaconSensor",
                    "location": [0,0,0],
                    "configuration": {
                        "id": 0
                    }
                },
            ],
            "control_scheme": 0,
            "location": [0, 0, -5]
        },
        {
            "agent_name": "auv1",
            "agent_type": "HoveringAUV",
            "sensors": [
                {
                    "sensor_type": "AcousticBeaconSensor",
                    "location": [0,0,0],
                    "configuration": {
                        "id": 1
                    }
                },
            ],
            "control_scheme": 0,
            "location": [0, 100, -5]
        }
    ]
}

env = holoocean.make(scenario_cfg=cfg)
env.reset()

# This is how you send a message from one acoustic com to another
# This sends from id 0 to id 1 (ids configured above)
# with message type "OWAY" and data "my_data_payload"
env.send_acoustic_message(0, 1, "OWAY", "my_data_payload")

for i in range(300):
    states = env.tick()
    if "AcousticBeaconSensor" in states['auv1']:
        # For this message, should receive back [message_type, from_sensor, data_payload]
        print(i, "Received:", states['auv1']["AcousticBeaconSensor"])
        break
    else:
        print(i, "No message received")