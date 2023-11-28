import paho.mqtt.publish as publish
import paho.mqtt.client as paho
import random
import json, dataclasses
import time
from mqtt import connect_mqtt

trackers = ["seguidor1", "seguidor2", "seguidor3", "seguidor4"]
device_ports = [1,2,3,4]
topics = []
variable_names = ["Irradiancia", "Temperatura ambiente", "Voltaje panel", "Corriente panel", "Angulo elevacion", "Angulo acimutal", "Voltaje motor", "Corriente motor"]
to_send_values = {}

# Configura los parámetros
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
    ang_elev = random.randint(0,90)
    ang_acimut = random.randint(0,360)
    volt_motor = random.randint(0,24)
    corr_motor = random.randint(0,3)
    
    var_values = [irradiancia, tempr, volt_panel, corr_panel, ang_elev, ang_acimut, volt_motor, corr_motor]

    for i in range (len(variable_names)):
        to_send_values[variable_names[i]] = var_values[i]
    

def send_variables(client):
    #MIRAR SI SE PUEDE HACER MAS REALISTA MIRANDO LA HORA DEL DIA PARA ESTIMAR LAS VARIABLES.
    while True:
        client.publish(topics[random.randint(0,len(topics-1))], json.dumps(to_send_values, cls=JSONEncoder))
        print("New variables sent")
        time.sleep(60)      #POSIBLE PUNTO DE ESTANCAMIENTO!!!!!!!!!!!!!!!!

def main():
    mqtt_client = connect_mqtt(
        BROKER,
        port,
        client_id = "raspberry",
        username="",
        password=""
    )
    build_topics()
    assign_variables()
    send_variables(mqtt_client)

# Publica el mensaje
#publish.single(topic, message, hostname=broker_address, auth={'username': username, 'password': password})
