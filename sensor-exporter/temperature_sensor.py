import logging
import adafruit_dht

class TemperatureSensorDHT22:
    def __init__(self, name, pin, metrics_exporter):
        self.name = name
        self.sensor = adafruit_dht.DHT22(pin)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.temperature_metric = metrics_exporter.register_sensor(name, "temperature")
        self.humidity_metric = metrics_exporter.register_sensor(name, "humidity")
        self.logger.info("Temperature sensor initialized on pin %s", pin)

    def read(self):
        try:
            temperature = self.sensor.temperature
            humidity = self.sensor.humidity
            self.logger.info("%s; Temperature: %s°C, Humidity: %s%%", self.name, temperature, humidity)

            if temperature is not None:
                self.temperature_metric.set(temperature)
            else:
                self.temperature_metric.set(float('nan'))
            if humidity is not None:
                self.humidity_metric.set(humidity)
            else:
                self.humidity_metric.set(float('nan'))

            return temperature, humidity
        except RuntimeError as error:
            self.logger.warning("Error reading from sensor: %s", error)
            self.temperature_metric.set(float('nan'))
            self.humidity_metric.set(float('nan'))
            return None, None

    def cleanup(self):
        self.sensor.exit()
        self.logger.info("Temperature sensor GPIO cleaned up")
