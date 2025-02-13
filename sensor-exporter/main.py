import logging
import time
import board
import settings
import signal
import busio
import adafruit_ads1x15.ads1115 as ADS
from soil_moisture_sensor import SoilMoistureSensor
from prometheus_client import start_http_server
from temperature_sensor import TemperatureSensorDHT22
from metrics_exporter import MetricsExporter

logging.basicConfig(level=logging.INFO)

def signal_handler(sig, frame):
    logger.info("Signal received: %s", sig)
    sensor1.cleanup()
    sensor2.cleanup()
    soil_sensor1.cleanup()
    soil_sensor2.cleanup()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    metrics_exporter = MetricsExporter()

    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)

    sensor1_pin = getattr(board, f"D{settings.TEMPERATURE_SENSOR_1_PIN}")
    sensor2_pin = getattr(board, f"D{settings.TEMPERATURE_SENSOR_2_PIN}")

    soil_sensor1 = SoilMoistureSensor("SoilSensor1", ads, ADS.P0, metrics_exporter)
    soil_sensor2 = SoilMoistureSensor("SoilSensor2", ads, ADS.P1, metrics_exporter)

    sensor1 = TemperatureSensorDHT22("Sensor1", sensor1_pin, metrics_exporter)
    sensor2 = TemperatureSensorDHT22("Sensor2", sensor2_pin, metrics_exporter)

    start_http_server(8000)
    try:
        while True:
            sensor1.read()
            sensor2.read()
            soil_sensor1.read()
            soil_sensor2.read()
            time.sleep(30)
    except KeyboardInterrupt:
        logging.info("Shutting down gracefully.")
    finally:
        sensor1.cleanup()
        sensor2.cleanup()
        soil_sensor1.cleanup()
        soil_sensor2.cleanup()
