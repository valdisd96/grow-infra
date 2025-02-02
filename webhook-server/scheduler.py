import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

class DeviceScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.devices = {}
        self.scheduler.start()

    def add_device(self, name, relay, on_time="06:00", off_time="00:00"):
        """
        Adds a new device to the scheduler.
        :param name: The name of the device (e.g. "light", "fan").
        :param relay: The relay object.
        :param on_time: The on time (default 06:00).
        :param off_time: The off time (default 00:00).
        """
        if name in self.devices:
            logging.warning(f"Device {name} already exists. Updating schedule.")
            self.update_schedule(name, on_time, off_time)
            return

        self.devices[name] = {"relay": relay, "on_time": on_time, "off_time": off_time}
        self._setup_jobs(name)

    def _setup_jobs(self, name):
        """Creates tasks for the specified device."""
        if name not in self.devices:
            logging.error(f"Device {name} not found!")
            return

        self.scheduler.remove_all_jobs(jobstore=name)
        device = self.devices[name]

        self.scheduler.add_job(
            self.turn_on_device, CronTrigger.from_crontab(f"{device['on_time']} * * *"),
            args=[name], id=f"{name}_on", replace_existing=True, jobstore=name
        )
        self.scheduler.add_job(
            self.turn_off_device, CronTrigger.from_crontab(f"{device['off_time']} * * *"),
            args=[name], id=f"{name}_off", replace_existing=True, jobstore=name
        )

        logging.info(f"Scheduled {name}: ON at {device['on_time']}, OFF at {device['off_time']}")

    def turn_on_device(self, name):
        """Turns on the device according to a schedule."""
        if name in self.devices:
            logging.info(f"Turning {name} ON")
            self.devices[name]["relay"].set_state(True)

    def turn_off_device(self, name):
        """Turns off the device according to a schedule."""
        if name in self.devices:
            logging.info(f"Turning {name} OFF")
            self.devices[name]["relay"].set_state(False)

    def update_schedule(self, name, on_time, off_time):
        """Updates the schedule for the specified device."""
        if name not in self.devices:
            logging.error(f"Device {name} not found!")
            return

        self.devices[name]["on_time"] = on_time
        self.devices[name]["off_time"] = off_time
        self._setup_jobs(name)
        logging.info(f"Updated schedule for {name}: ON at {on_time}, OFF at {off_time}")

    def shutdown(self):
        """Stops the scheduler when it terminates."""
        self.scheduler.shutdown()
