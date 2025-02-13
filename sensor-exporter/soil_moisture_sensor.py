import logging
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class SoilMoistureSensor:
    def __init__(self, name, ads, channel, metrics_exporter):
        self.name = name
        self.ads = ads
        self.channel = AnalogIn(self.ads, channel)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.metrics_exporter = metrics_exporter
        self.logger.info("Soil moisture sensor initialized on %s", channel)


    def read(self):
        try:
            moisture_value = self.channel.value
            voltage = self.channel.voltage

            self.logger.info("%s; Raw value: %d, Voltage: %.3fV", self.name, moisture_value, voltage)

            if moisture_value is not None:
                self.metrics_exporter.update_metric(self.name, "soil_moisture", moisture_value)
            else:
                self.metrics_exporter.update_metric(self.name, "soil_moisture", float('nan'))

            return moisture_value, voltage
        except Exception as error:
            self.logger.warning("Error reading from soil moisture sensor: %s", error)
            self.metrics_exporter.update_metric(self.name, "soil_moisture", float('nan'))
            return None, None

    def cleanup(self):
        self.logger.info("Soil moisture sensor %s cleanup complete.", self.name)
