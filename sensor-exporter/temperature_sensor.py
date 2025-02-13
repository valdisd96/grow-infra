import logging
import adafruit_dht

class TemperatureSensorDHT22:
    def __init__(self, name, pin, metrics_exporter):
        self.name = name
        self.sensor = adafruit_dht.DHT22(pin)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.metrics_exporter = metrics_exporter
        self.logger.info("Temperature sensor initialized on pin %s", pin)

    def read(self):
        try:
            temperature = self.sensor.temperature
            humidity = self.sensor.humidity
            self.logger.info("%s; Temperature: %s°C, Humidity: %s%%", self.name, temperature, humidity)

            if temperature is not None:
                self.metrics_exporter.update_metric(self.name, "temperature_inside", temperature)
            else:
                self.metrics_exporter.update_metric(self.name, "temperature_inside", float('nan'))
            if humidity is not None:
                self.metrics_exporter.update_metric(self.name, "humidity_inside", humidity)
            else:
                self.metrics_exporter.update_metric(self.name, "humidity_inside", float('nan'))

            return temperature, humidity
        except RuntimeError as error:
            self.logger.warning("Error reading from sensor: %s", error)
            self.metrics_exporter.update_metric(self.name, "temperature_inside", float('nan'))
            self.metrics_exporter.update_metric(self.name, "humidity_inside", float('nan'))
            return None, None

    def cleanup(self):
        self.sensor.exit()
        self.logger.info("Temperature sensor GPIO cleaned up")
