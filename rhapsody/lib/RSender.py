from paho.mqtt import client as mqtt_client
import uuid


class Sender:
    broker = None
    port = None
    client_id = f'rhapsody-mqtt-{uuid.uuid4()}'
    client = None

    def connect(self, client, userdata, flags, rc):
        if(rc == 0):
            print("Connecté au broker MQTT")
        else:
            print("La connection a échouée. Code %d\n", rc)


    def __init__(self, broker, port = 1883):
        self.broker = broker
        self.port = port

        self.client = mqtt_client.Client(self.client_id)
        #print(type(self.client))
        self.client.on_connect = self.connect


    def publish(self, topic, message):
        self.client.connect(self.broker, self.port)
        result = self.client.publish(topic, message, 1)
        status = result[0]
        if(status != 0):
            print("Impossible d'envoyer l'instruction. Voir logs")
