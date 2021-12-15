import paho.mqtt.client as mqtt
import uuid
import json
import threading
from datetime import datetime




class Monitoring(threading.Thread):

    broker = None
    port = None
    client_id = f'rhapsody-monitoring-{uuid.uuid4()}'
    client = None
    project_id = None


    def connect(self, client, userdate, flags, rc):
        if(rc == 0):
            print("Connecé au broker MQTT")
        else:
            print("La connection a échouée. Code %d\b", rc)


    # Initialization
    def __init__(self, project_id, broker, port = 1883):
        threading.Thread.__init__(self)

        self.broker = broker
        self.port = port

        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self.connect
        self.client.connect(self.broker, self.port)

        self.project_id = project_id


    def run(self):
        while 1:
            self.client.loop()


    # Envoie du message
    def send(self, message_type, message_origin, message_content):

        # Récupération des données à envoyer
        message = dict()
        message['message_type'] = message_type
        message['message_datetime'] = str(datetime.now())
        message['message_origin'] = message_origin
        message['message_content'] = message_content
        message_to_send = json.dumps(message)

        # Envoie du message
        print("Sending message")
        self.client.publish("rhapsody/monitoring/" + self.project_id, message_to_send)


