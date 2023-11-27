import paho.mqtt.publish as publish
import paho.mqtt.client as paho
import random

panels = ["panel1", "panel2", "panel3", "panel4"]
motors = ["motor1", "motor2", "motor3", "motor4"]
device_ports = [1,2,3,4]
topics = []
panel_variables = ["Irradiancia", "Temperatura ambiente", "Voltaje panel", "Corriente panel"]
motor_variables = ["Angulo elevacion", "Angulo acimutal", "Voltaje motor", "Corriente motor"]

def build_topics():
    
    for i in range(len(panels)):
        current_port = device_ports[random.randint(0, len(device_ports)-1)]
        topics.append(panels[i] + "/" + str(current_port))
        topics.append(motors[i] + "/" + str(current_port))
        device_ports.remove(current_port)
        

def send_variables(variable):
    irradiancia = random.randint(0,1500)
    tempr = random.randint(-10,70)
    volt_panel = random.randint(0,25)
    corr_panel = random.randint(0,5)

    ang_elev = random.randint(0,90)
    ang_acimut = random.randint(0,360)
    volt_motor = random.randint(0,24)
    corr_motor = random.randint(0,3)

    


    #Tengo que usar diccionarios para enviar variable:valor a formato JSON -> Guiarme de monitor.py Juan
    #El metodo publish de paho.mqtt al parecer me permite formatear diccionarios a JSON!
    print("kha")






build_topics()
for i in range(len(topics)):
    print("El tema #" +str(i)+ " es " + topics[i])



# Configura los parámetros
#broker_address = "172.24.100.204"
#port = 8081
#message = "<mensaje>"
#username = ""
#password = ""

#client1 = paho.Client("raspberry")
#client1.connect(broker_address, port)


# Publica el mensaje
#publish.single(topic, message, hostname=broker_address, auth={'username': username, 'password': password})
