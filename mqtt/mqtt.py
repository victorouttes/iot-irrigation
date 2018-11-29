import paho.mqtt.client as mqttclient
import ssl

TOPICS = 'iot'
RECONNECT_DELAY_SECS = 2


def on_connect(client, userdata, flags, rc):
    if userdata == 0:
        print('First connection!')
        client.subscribe(TOPICS, qos=1)
    else:
        print('Reconnection!')


def on_message(client, userdata, msg):
    from home.models import Sensor
    print(msg.topic + " " + str(msg.qos) + " " + msg.payload.decode("utf-8"))
    try:
        data = msg.payload.decode("utf-8").split(';')
        sensor = Sensor()
        sensor.humidity = data[0]
        sensor.temperature = data[1]
        sensor.sunlight = data[2]
        sensor.save()
    except Exception as e:
        print(e + ' - ' + e.message)


def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_disconnect(client, userdata, rc):
    client.user_data_set(userdata + 1)
    if userdata == 0:
        client.reconnect()


def run():
    client = mqttclient.Client(client_id='server-iot-home', clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    client.user_data_set(0)
    #client.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2,
    #               ciphers=None)
    client.username_pw_set('unibratec', password='unibratec')
    client.connect('mqtt.victorouttes.com.br', 1883, 60)
    client.loop_start()
