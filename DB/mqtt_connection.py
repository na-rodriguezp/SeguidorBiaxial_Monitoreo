from paho.mqtt import client as mqtt_client
import time
import random

# generate client ID with pub prefix randomly

def connect_mqtt(broker, port, client_id, username, password):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Mosquitto Broker!")
        else:
            print("Failed to connect, return code %d", rc)
    
    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection.")

    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect #                          POSIBLE PUNTO DE FALLA
    client.on_disconnect = on_disconnect #                    POSIBLE PUNTO DE FALLA
    client.connect(broker, port)
    
    return client