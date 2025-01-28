from prometheus_client import Gauge

class MetricsExporter:
    def __init__(self):
        self.temperature_metric = Gauge(
            "temperature_inside",
            "Temperature metrics from all sensors",
            ["sensor"]
        )
        self.humidity_metric = Gauge(
            "humidity_inside",
            "Humidity metrics from all sensors",
            ["sensor"]
        )
        self.metrics = {}

    def set_temperature(self, sensor_name, value):
        self.temperature_metric.labels(sensor=sensor_name).set(value)

    def set_humidity(self, sensor_name, value):
        self.humidity_metric.labels(sensor=sensor_name).set(value)

    def register_sensor(self, sensor_name, metric_type="metric"):
        metric_key = f"{metric_type}_{sensor_name}"
        if metric_key not in self.metrics:
            self.metrics[metric_key] = Gauge(metric_key, f"{metric_type.capitalize()} metric for {sensor_name}")
        return self.metrics[metric_key]

    def update_metric(self, sensor_name, metric_type, value):
        metric_key = f"{metric_type}_{sensor_name}"
        if metric_key in self.metrics:
            self.metrics[metric_key].set(value)
