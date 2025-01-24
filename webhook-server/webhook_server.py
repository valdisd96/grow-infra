import logging
import subprocess
import settings
import signal
from relay import Relay
from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("WebhookServer")

def signal_handler(sig, frame):
    logger.info("Signal received: %s", sig)
    funRelay.cleanup()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

@app.route('/fan-control', methods=['POST'])
def fan_control():
    try:
        data = request.json
        logger.info(f"Received alert: {data}")

        for alert in data.get("alerts", []):
            state = alert["labels"].get("state")
            if state == "on":
                logger.info("Turning fan ON")
                funRelay.set_state(True)
            elif state == "off":
                logger.info("Turning fan OFF")
                funRelay.set_state(False)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Error processing alert: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    try:
        relay_pin = settings.RELAY_PIN
        funRelay = Relay("FanRelay", relay_pin)

        logger.info("Starting Flask server on port 8080.")
        app.run(host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        funRelay.cleanup()