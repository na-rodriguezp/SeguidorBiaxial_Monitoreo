import paho.mqtt.publish as publish
import paho.mqtt.client as paho
import random
import json, dataclasses
import time
from mqtt_connection import connect_mqtt

trackers = ["seguidor1", "seguidor2", "seguidor3", "seguidor4"]
device_ports = [1,2,3,4]
topics = []
variable_names = ["Irradiancia", "Temperatura ambiente", "Voltaje panel", "Corriente panel", "Potencia panel", "Angulo elevacion", "Angulo acimutal", "Voltaje motores", "Corriente motores", "Potencia motores"]
to_send_values = {}

BROKER = "172.24.100.204"
port = 8081

def build_topics():
    for i in range(len(trackers)):
        current_port = device_ports[random.randint(0, len(device_ports)-1)]
        topics.append(trackers[i] + "/" + str(current_port))
        device_ports.remove(current_port)


class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            try:
                return super().default(o)
            except TypeError:
                return str(o)
        

def assign_variables():
    irradiancia = random.randint(0,1500)
    tempr = random.randint(-10,70)
    volt_panel = random.randint(0,25)
    corr_panel = random.randint(0,5)
    pot_panel = volt_panel*corr_panel
    ang_elev = random.randint(0,90)
    ang_acimut = random.randint(0,360)
    volt_motores = random.randint(0,24)
    corr_motores = random.randint(0,3)
    pot_motores = volt_motores*corr_motores
    
    var_values = [irradiancia, tempr, volt_panel, corr_panel, pot_panel, ang_elev, ang_acimut, volt_motores, corr_motores, pot_motores]

    for i in range (len(variable_names)):
        to_send_values[variable_names[i]] = var_values[i]
    

def send_variables(client):
    while True:
        random.shuffle(topics)
        print("The first topic in the list is " + topics[0])
        for topic in topics:
            assign_variables()
            client.publish(topic, json.dumps(to_send_values, cls=JSONEncoder))
        print("New variables sent")
        time.sleep(60)

def main():
    mqtt_client = connect_mqtt(
        BROKER,
        port,
        client_id = "raspberry",
        username="",
        password=""
    )
    build_topics()
    send_variables(mqtt_client)


main()
