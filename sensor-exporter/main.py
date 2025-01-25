import logging
import time
import board
import settings
import signal
from prometheus_client import start_http_server
from temperature_sensor import TemperatureSensorDHT22
from metrics_exporter import MetricsExporter

logging.basicConfig(level=logging.INFO)

def signal_handler(sig, frame):
    logger.info("Signal received: %s", sig)
    sensor1.cleanup()
    sensor2.cleanup()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    metrics_exporter = MetricsExporter()

    sensor1_pin = getattr(board, f"D{settings.TEMPERATURE_SENSOR_1_PIN}")
    sensor2_pin = getattr(board, f"D{settings.TEMPERATURE_SENSOR_2_PIN}")

    sensor1 = TemperatureSensorDHT22("Sensor1", sensor1_pin, metrics_exporter)
    sensor2 = TemperatureSensorDHT22("Sensor2", sensor2_pin, metrics_exporter)

    start_http_server(8000)
    try:
        while True:
            sensor1.read()
            sensor2.read()
            time.sleep(30)
    except KeyboardInterrupt:
        logging.info("Shutting down gracefully.")
    finally:
        sensor1.cleanup()
        sensor2.cleanup()
