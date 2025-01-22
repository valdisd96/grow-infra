from prometheus_client import Gauge, start_http_server

# Температура и влажность
TEMPERATURE_SENSOR_1 = Gauge("temperature_sensor_1", "Temperature from sensor 1")
HUMIDITY_SENSOR_1 = Gauge("humidity_sensor_1", "Humidity from sensor 1")
TEMPERATURE_SENSOR_2 = Gauge("temperature_sensor_2", "Temperature from sensor 2")
HUMIDITY_SENSOR_2 = Gauge("humidity_sensor_2", "Humidity from sensor 2")

# Средние значения
AVG_TEMPERATURE = Gauge("avg_temperature", "Average temperature from all sensors")
AVG_HUMIDITY = Gauge("avg_humidity", "Average humidity from all sensors")

# Состояние реле
RELAY_STATE = Gauge("relay_state", "State of the relay: 1 for ON, 0 for OFF")

# Запустите HTTP-сервер для Prometheus
def start_metrics_server(port=8000):
    start_http_server(port)
