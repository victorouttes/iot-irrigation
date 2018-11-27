from django.apps import AppConfig


class MqttConfig(AppConfig):
    name = 'mqtt'

    def ready(self):
        from . import mqtt
        mqtt.run()
