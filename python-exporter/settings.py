import os

# Pin configurations
TEMPERATURE_LED_PIN = int(os.environ.get("TEMPERATURE_LED_PIN", 0))
TEMPERATURE_SENSOR_1_PIN = int(os.environ.get("TEMPERATURE_SENSOR_1_PIN", 26))
TEMPERATURE_SENSOR_2_PIN = int(os.environ.get("TEMPERATURE_SENSOR_2_PIN", 19))

# Relay
RELAY_PIN = int(os.environ.get("RELAY_PIN", 6))

# Thresholds
TEMPERATURE_THRESHOLD = float(os.environ.get("TEMPERATURE_THRESHOLD", 22.2))
HUMIDITY_THRESHOLD = float(os.environ.get("HUMIDITY_THRESHOLD", 30.0))

# Other configurations (optional)
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

# Telegram bot settings
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

#ultrasonic detector
ULTRASONIC_ECHO_PIN = int(os.environ.get("ULTRASONIC_ECHO_PIN", 0))
ULTRASONIC_TRIG_PIN = int(os.environ.get("ULTRASONIC_TRIG_PIN", 0))
ULTRASONIC_LED_PIN = int(os.environ.get("ULTRASONIC_LED_PIN", 0))