import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

class DeviceScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.devices = {}
        self.scheduler.start()

    def check_initial_state(self):
        """checks whether the device should be turned on when the program starts"""
        now = datetime.now().time()
        print(now)
        print(self.devices.items())
        for device_name, device_info in self.devices.items():
            print(device_name, device_info)
            if device_info.get("on_time") and device_info.get("off_time"):
                print(device_info.get("on_time"), "ON TIME!!!")
                on_time = datetime.strptime(device_info["on_time"], "%H:%M").time()
                off_time = datetime.strptime(device_info["off_time"], "%H:%M").time()
                now_now = datetime.strptime(now, "%H:%M").time()
                print(on_time, off_time)

                if on_time <= now_now <= off_time:
                    print("fuck")
                    device_info["relay"].set_state(True)
                    logging.info(f"{device_info['relay'].name}: Staste ON")
                else:
                    device_info["relay"].set_state(False)
                    logging.info(f"{device_info['relay'].name}: Staste OFF")

    def add_device(self, name, relay, on_time=None, off_time=None, repeat_interval_hours=None, on_duration_minutes=None):
        """
        Adds a device to the schedule.
        :param name: Device name (e.g. "light", "fan").
        :param relay: Relay object.
        :param on_time: Turn-on time.
        :param off_time: Shutdown time.
        :param repeat_interval_hours: Repeat every X hours (optional).
        :param on_duration_minutes: Turn on for Y minutes when repeating (optional).
        """
        if name in self.devices:
            logging.warning(f"Device {name} has already been added. Updating schedule.")
            self.update_schedule(name, on_time, off_time, repeat_interval_hours, on_duration_minutes)
            return

        self.devices[name] = {
            "relay": relay,
            "on_time": on_time,
            "off_time": off_time,
            "repeat_interval_hours": repeat_interval_hours,
            "on_duration_minutes": on_duration_minutes,
        }
        self._setup_jobs(name)
        self.check_initial_state()

    def _setup_jobs(self, name):
        """Creates scheduled tasks for the device."""
        if name not in self.devices:
            logging.error(f"Device {name} not found!")
            return

        device = self.devices[name]

        self.scheduler.remove_all_jobs(jobstore=name)

        if device["repeat_interval_hours"] and device["on_duration_minutes"]:
            self.add_recurring_job(name, device["repeat_interval_hours"], device["on_duration_minutes"])
        else:
            self.scheduler.add_job(
                self.turn_on_device,
                CronTrigger(hour=int(device["on_time"].split(":")[0]), minute=int(device["on_time"].split(":")[1])),
                args=[name],
                id=f"{name}_on",
                replace_existing=True
            )
            self.scheduler.add_job(
                self.turn_off_device,
                CronTrigger(hour=int(device["off_time"].split(":")[0]), minute=int(device["off_time"].split(":")[1])),
                args=[name],
                id=f"{name}_off",
                replace_existing=True
            )

        logging.info(f"Scheduled {name}: ON at {device['on_time']}, OFF at {device['off_time']}, repeat hours: {device['repeat_interval_hours']}, active minutes: {device['on_duration_minutes']}")

    def add_recurring_job(self, name, repeat_interval_hours, on_duration_minutes):
        """Adds a repeating task to run for X minutes every Y hours."""
        self.scheduler.add_job(
            self.turn_on_device,
            IntervalTrigger(hours=repeat_interval_hours),
            args=[name],
            id=f"{name}_recurring_on",
            replace_existing=True
        )

        self.scheduler.add_job(
            self.turn_off_device,
            IntervalTrigger(hours=repeat_interval_hours, minutes=on_duration_minutes),
            args=[name],
            id=f"{name}_recurring_off",
            replace_existing=True
        )

        logging.info(f"Device {name} will turn on for {on_duration_minutes} minutes every {repeat_interval_hours} hours.")

    def turn_on_device(self, name):
        """Turns on the device."""
        if name in self.devices:
            logging.info(f"Turn on {name}")
            self.devices[name]["relay"].set_state(True)

    def turn_off_device(self, name):
        """Turns off the device."""
        if name in self.devices:
            logging.info(f"Turn off {name}")
            self.devices[name]["relay"].set_state(False)

    def update_schedule(self, name, on_time, off_time, repeat_interval_hours=None, on_duration_minutes=None):
        """Updates the device schedule."""
        if name not in self.devices:
            logging.error(f"Device {name} not found!")
            return

        self.devices[name]["on_time"] = on_time
        self.devices[name]["off_time"] = off_time
        self.devices[name]["repeat_interval_hours"] = repeat_interval_hours
        self.devices[name]["on_duration_minutes"] = on_duration_minutes
        self._setup_jobs(name)
        logging.info(f"Updated schedule {name}: ON at {on_time}, OFF at {off_time}")

    def shutdown(self):
        """Stops the scheduler."""
        self.scheduler.shutdown()
