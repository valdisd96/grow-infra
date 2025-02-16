import logging
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class SoilMoistureSensor:
    def __init__(self, name, ads, channel, metrics_exporter, dry_value, wet_value):

        """
        :param name: Sensor name
        :param ads: instance of ADS1115
        :param channel: Chanell of ADS1115 (ex.: ADS.P0)
        :param metrics_exporter: Instance of MetricsExporter
        :param dry_value: Sendor dry value
        :param wet_value: Sensor value in water
        """

        self.name = name
        self.ads = ads
        self.channel = AnalogIn(self.ads, channel)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.metrics_exporter = metrics_exporter
        self.dry_value = dry_value
        self.wet_value = wet_value
        self.logger.info("Soil moisture sensor initialized on %s", channel)


    def read(self):
        try:
            moisture_value = self.channel.value
            voltage = self.channel.voltage

            moisture_percentage = self.convert_to_percentage(moisture_value)

            self.logger.info(
                "%s; Raw value: %d, Voltage: %.3fV, Percentage: %.1f%%",
                self.name, moisture_value, voltage, moisture_percentage
            )

            if moisture_percentage is not None:
                self.metrics_exporter.update_metric(self.name, "soil_moisture", moisture_percentage)
            else:
                self.metrics_exporter.update_metric(self.name, "soil_moisture", float('nan'))

            return moisture_percentage
        except Exception as error:
            self.logger.warning("Error reading from soil moisture sensor: %s", error)
            self.metrics_exporter.update_metric(self.name, "soil_moisture", float('nan'))
            return None, None

    def convert_to_percentage(self, moisture_value):
        if moisture_value is None:
            return None

        if moisture_value > self.dry_value:
            moisture_value = self.dry_value
        elif moisture_value < self.wet_value:
            moisture_value = self.wet_value
        return 100 * (1 - (moisture_value - self.wet_value) / (self.dry_value - self.wet_value))

    def cleanup(self):
        self.logger.info("Soil moisture sensor %s cleanup complete.", self.name)
