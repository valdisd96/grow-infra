import logging
import requests
import RPi.GPIO as GPIO
import settings
from metrics import RELAY_STATE

class Relay:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.state = False 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("%s relay initialized on pin %s", name, pin)

    def send_telegram_message(self, message):
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": settings.TELEGRAM_CHAT_ID, "text": message}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            self.logger.info("Message sent to Telegram: %s", message)
        except requests.exceptions.RequestException as e:
            self.logger.warning("Failed to send Telegram message: %s", e)

    def set_state(self, state):
        if self.state != state:
            self.state = state
            GPIO.output(self.pin, GPIO.HIGH if state else GPIO.LOW)
            state_str = "ON" if state else "OFF"
            self.logger.info("%s relay state set to %s", self.name, state_str)
            self.send_telegram_message(f"{self.name} relay state changed to {state_str}")

    def set_state(self, state):
        if self.state != state:
            self.state = state
            GPIO.output(self.pin, GPIO.HIGH if state else GPIO.LOW)
            state_str = "ON" if state else "OFF"
            self.logger.info("%s relay state set to %s", self.name, state_str)
            self.send_telegram_message(f"{self.name} relay state changed to {state_str}")
            RELAY_STATE.set(1 if state else 0)

    def cleanup(self):
        GPIO.output(self.pin, GPIO.LOW)
        GPIO.cleanup(self.pin)
        self.logger.info("%s relay GPIO cleaned up", self.name)
