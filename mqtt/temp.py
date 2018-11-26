import paho.mqtt.client as mqtt
import time, ssl


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, outro):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("topico/#")


def on_disconnect(a, b, c):
	print('desconectado!')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def on_log(client, userdata, level, buf):
    print("log: ", buf)


print('Comecando...')
client = mqtt.Client(client_id='ABCD')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_log = on_log
client.on_message = on_message
client.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client.username_pw_set('unibratec', password='unibratec')
client.connect('mqtt.victorouttes.com.br', 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()
time.sleep(100)

