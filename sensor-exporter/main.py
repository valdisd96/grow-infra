import logging
import time
import board
import settings
from prometheus_client import start_http_server
from relay import Relay
from temperature_sensor import TemperatureSensorDHT22
from metrics_exporter import MetricsExporter

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    metrics_exporter = MetricsExporter()

    relay_pin = settings.RELAY_PIN
    sensor1_pin = getattr(board, f"D{settings.TEMPERATURE_SENSOR_1_PIN}")
    sensor2_pin = getattr(board, f"D{settings.TEMPERATURE_SENSOR_2_PIN}")

    relay = Relay("FanRelay", relay_pin)
    sensor1 = TemperatureSensorDHT22("Sensor1", sensor1_pin, metrics_exporter)
    sensor2 = TemperatureSensorDHT22("Sensor2", sensor2_pin, metrics_exporter)

    start_http_server(8000)
    try:
        while True:
            sensor1.read()
            sensor2.read()
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Shutting down gracefully.")
    finally:
        sensor1.cleanup()
        sensor2.cleanup()
        relay.cleanup()
