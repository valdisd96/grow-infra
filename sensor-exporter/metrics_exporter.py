from prometheus_client import Gauge

class MetricsExporter:
    def __init__(self):
        self.metrics = {}

    def register_sensor(self, metric_type):
        if metric_type not in self.metrics:
            self.metrics[metric_type] = Gauge(
                metric_type,
                f"{metric_type.replace('_', ' ').capitalize()} metric from all sensors",
                ["sensor"]
            )
        return self.metrics[metric_type]

    def update_metric(self, sensor_name, metric_type, value):
        if metric_type not in self.metrics:
            self.register_sensor(metric_type)

        self.metrics[metric_type].labels(sensor=sensor_name).set(value)
