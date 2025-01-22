import logging
import adafruit_dht
from metrics import TEMPERATURE_SENSOR_1, HUMIDITY_SENSOR_1, TEMPERATURE_SENSOR_2, HUMIDITY_SENSOR_2

class TemperatureSensor:
    def __init__(self, name, pin):
        self.name = name
        self.sensor = adafruit_dht.DHT22(pin)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Temperature sensor initialized on pin %s", pin)

    def read(self):
        try:
            temperature = self.sensor.temperature
            humidity = self.sensor.humidity
            self.logger.info("%s; Temperature: %s°C, Humidity: %s%%", self.name, temperature, humidity)
            if self.name == "Sensor1":
                TEMPERATURE_SENSOR_1.set(temperature)
                HUMIDITY_SENSOR_1.set(humidity)
            elif self.name == "Sensor2":
                TEMPERATURE_SENSOR_2.set(temperature)
                HUMIDITY_SENSOR_2.set(humidity)

            return temperature, humidity
        except RuntimeError as error:
            self.logger.warning("Error reading from sensor: %s", error)
            return None, None

    def cleanup(self):
        self.sensor.exit()  # Release DHT sensor resources
        self.logger.info("Temperature sensor GPIO cleaned up")