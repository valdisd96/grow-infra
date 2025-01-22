from prometheus_client import Gauge

class MetricsExporter:
    def __init__(self):
        self.metrics = {}

    def register_sensor(self, name, metric_type="temperature"):
        metric_key = f"{metric_type}_{name}"
        if metric_key not in self.metrics:
            self.metrics[metric_key] = Gauge(metric_key, f"{metric_type.capitalize()} metric for {name}")
        return self.metrics[metric_key]

    def update_metric(self, name, metric_type, value):
        metric_key = f"{metric_type}_{name}"
        if metric_key in self.metrics:
            self.metrics[metric_key].set(value)
