import logging
import RPi.GPIO as GPIO

class Relay:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("%s relay initialized on pin %s", name, pin)

    def set_state(self, state):
        GPIO.output(self.pin, GPIO.HIGH if state else GPIO.LOW)
        self.logger.info("%s relay state set to %s", self.name, "ON" if state else "OFF")

    def cleanup(self):
        GPIO.output(self.pin, GPIO.LOW)
        GPIO.cleanup(self.pin)
        self.logger.info("%s relay GPIO cleaned up", self.name)
