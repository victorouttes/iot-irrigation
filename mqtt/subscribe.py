import paho.mqtt.client as mqtt
from .models import ConfigMQTT


def on_connect(client, userdata, flags, rc):
    client.subscribe('topico')


def on_message(client, userdata, msg):
    print(msg.topic + ' - ' + str(msg.payload))


def main(config: ConfigMQTT):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(config.username, config.password)
    client.connect(config.host, int(config.port))
    client.loop_forever()

