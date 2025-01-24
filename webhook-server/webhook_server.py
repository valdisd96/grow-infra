import logging
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("WebhookServer")

FAN_CONTROL_SCRIPT = "scripts/fan_control.sh"

@app.route('/fan-control', methods=['POST'])
def fan_control():
    try:
        data = request.json
        logger.info(f"Received alert: {data}")

        for alert in data.get("alerts", []):
            state = alert["labels"].get("state")
            if state == "on":
                logger.info("Turning fan ON")
                subprocess.run([FAN_CONTROL_SCRIPT, "on"], check=True)
            elif state == "off":
                logger.info("Turning fan OFF")
                subprocess.run([FAN_CONTROL_SCRIPT, "off"], check=True)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Error processing alert: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
