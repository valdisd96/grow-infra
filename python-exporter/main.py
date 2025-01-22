import logging
import time
import settings
import board
from relay import Relay
import signal
import sys
from temperature_sensor import TemperatureSensor
from metrics import AVG_TEMPERATURE, AVG_HUMIDITY, start_metrics_server

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO)
)
logger = logging.getLogger(__name__)

def signal_handler(sig, frame):
    logger.info("Signal received: %s", sig)
    relay.cleanup()
    sensor1.cleanup()
    sensor2.cleanup()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    start_metrics_server(port=8000)

    relay_pin = settings.RELAY_PIN
    sensor1_pin = getattr(board, f"D{settings.TEMPERATURE_SENSOR_1_PIN}")
    sensor2_pin = getattr(board, f"D{settings.TEMPERATURE_SENSOR_2_PIN}")

    relay = Relay("FanRelay" ,relay_pin)
    sensor1 = TemperatureSensor("Sensor1", sensor1_pin)
    sensor2 = TemperatureSensor("Sensor2", sensor2_pin)

    try:
        while True:
            temp1, hum1 = sensor1.read()
            temp2, hum2 = sensor2.read()

            if temp1 is not None and hum1 is not None and temp2 is not None and hum2 is not None:
                avg_temp = (temp1 + temp2) / 2
                avg_hum = (hum1 + hum2) / 2

                AVG_TEMPERATURE.set(avg_temp)
                AVG_HUMIDITY.set(avg_hum)
                
                logger.info("Average Temperature: %.2f°C, Average Humidity: %.2f%%", avg_temp, avg_hum)

                if avg_temp > settings.TEMPERATURE_THRESHOLD and avg_hum > settings.HUMIDITY_THRESHOLD:
                    relay.set_state(True)
                else:
                    relay.set_state(False)
            else:
                logger.warning("Failed to read data from one or both sensors.")

            time.sleep(10)
    except KeyboardInterrupt:
        logger.info("Program stopped by user.")
    finally:
        # Ensure GPIOs are cleaned up
        relay.cleanup()
        sensor1.cleanup()
        sensor2.cleanup()