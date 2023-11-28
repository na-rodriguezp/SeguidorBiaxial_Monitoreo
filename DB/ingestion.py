from mqtt_connection import connect_mqtt
import db_utils as utils
import random
import json

BROKER = "localhost"
PORT = 8081
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = "biaxial"
password = "biaxialIOT2023"

def process_payload(topic:str, payload: str):
    data = json.loads(payload)

    topic_parts = topic.split('/')

    device_id = topic_parts[0]
    device_port = topic_parts[1]

    device = utils.get_or_create_device(device_id, device_port)

    for measure in data:
        try:
            measurement = utils.get_or_create_measurement(measure, measure, None, type(data[measure]) == str)
            value = data[measure]
            if type(value) == str:
                string_map = utils.get_or_create_string(measurement_id=measurement.id, string=value)
                value = string_map.value
            
            saved_value = utils.create_value(device_id=device.id, measurement_id=measurement.id, value=value)
            # print(f"Saved value: {saved_value.id if saved_value != None else -1}")
        except Exception as e:
            pass
            # print("ERROR in process_payload:")
            # print(topic)
            # print(measure, data[measure])

def process_mqtt_message(client, userdata, message):
    topic = message.topic
    try:
        payload = message.payload.decode()
        print(f"Received message from `{topic}` topic. Processing...")
        if len(topic.split('/')) == 2:
            process_payload(topic, payload)
        else:
            pass
            # print("Invalid topic. Skipping...")
            # print(f"Payload: {payload}")
    except Exception as e:
        print("ERROR in process_mqtt_message:")
        print(e)
        print(topic)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker :)!")
        client.on_message = process_mqtt_message
        client.subscribe("#")
    else:
        print("Failed to connect, return code %d", rc)

def run():
    client = connect_mqtt(BROKER, PORT, client_id, username, password)
    # client.on_message = process_mqtt_message
    # client.subscribe("#")
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    client.loop_forever()

if __name__ == '__main__':
    run()