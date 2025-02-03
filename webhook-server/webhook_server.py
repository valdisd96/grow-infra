import logging
import subprocess
import settings
import signal
from relay import Relay
from flask import Flask, request, jsonify
from scheduler import DeviceScheduler

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("WebhookServer")

def signal_handler(sig, frame):
    logger.info("Signal received: %s", sig)
    deviceScheduler.shutdown()
    funRelay.cleanup()
    lightRelay.cleanup()
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

@app.route('/set-schedule', methods=['POST'])
def set_schedule():
    """
    Expect JSON:
    {
        "name": "light",
        "on_time": "07:00",
        "off_time": "01:00",
        "repeat_interval_hours": 2,
        "on_duration_minutes": 5
    }
    """
    try:
        data = request.json
        name = data.get("name")
        on_time = data.get("on_time")
        off_time = data.get("off_time")
        repeat_interval_hours = data.get("repeat_interval_hours")
        on_duration_minutes = data.get("on_duration_minutes")

        if not name or not on_time or not off_time:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        if name not in deviceScheduler.devices:
            return jsonify({"status": "error", "message": f"Device {name} not found"}), 404

        deviceScheduler.update_schedule(name, on_time, off_time, repeat_interval_hours, on_duration_minutes)
        return jsonify({"status": "success", "name": name, "on_time": on_time, "off_time": off_time}), 200
    except Exception as e:
        logger.error(f"Error updating schedule: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/fan-control', methods=['POST'])
def fan_control():
    try:
        data = request.json
        logger.info(f"Fan-control Received alert: {data}")

        for alert in data.get("alerts", []):
            state = alert["status"]
            if state == "firing":
                logger.info("Turning fan ON")
                funRelay.set_state(True)
            elif state == "resolved":
                logger.info("Turning fan OFF")
                funRelay.set_state(False)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Error processing alert: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/light-control', methods=['POST'])
def light_control():
    try:
        data = request.json
        logger.info(f"Light-control Received alert: {data}")

        for alert in data.get("alerts", []):
            state = alert["status"]
            if state == "firing":
                logger.info("Turning fan ON")
                lightRelay.set_state(True)
            elif state == "resolved":
                logger.info("Turning fan OFF")
                lightRelay.set_state(False)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Error processing alert: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    try:
        light_relay_pin = settings.LIGHT_RELAY_PIN
        fun_relay_pin = settings.FUN_RELAY_PIN
        
        lightRelay = Relay("lightRelay", light_relay_pin)
        funRelay = Relay("FanRelay", fun_relay_pin)

        deviceScheduler = DeviceScheduler()
        deviceScheduler.add_device("light", lightRelay)
        deviceScheduler.add_device("fan", funRelay, repeat_interval_hours=1, on_duration_minutes=10)

        logger.info("Starting Flask server on port 8080.")
        app.run(host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        deviceScheduler.shutdown()
        funRelay.cleanup()
        lightRelay.cleanup()