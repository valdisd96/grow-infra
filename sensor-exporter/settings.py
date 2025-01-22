import os
TEMPERATURE_SENSOR_1_PIN = int(os.environ.get("TEMPERATURE_SENSOR_1_PIN", 26))
TEMPERATURE_SENSOR_2_PIN = int(os.environ.get("TEMPERATURE_SENSOR_2_PIN", 19))
RELAY_PIN = int(os.environ.get("RELAY_PIN", 6))