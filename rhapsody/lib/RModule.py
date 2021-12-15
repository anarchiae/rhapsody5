import requests
import threading
import lib.RSender as rsender
import lib.RMonitoring as rmonitoring
import time


class Module(threading.Thread):
    rmodule_type = None
    rmodule_id = None
    rmodule_values = None
    rmodule_mqtt_topic = None
    mqtt_sender = None
    monitoring = None


    def __init__(self, rmodule_type, rmodule_id, rmodule_mqtt_topic, project_id, broker, port = 1883):
        threading.Thread.__init__(self)

        self.monitoring = rmonitoring.Monitoring(project_id, broker)
        self.rmodule_type = rmodule_type
        self.rmodule_id = rmodule_id
        self.rmodule_mqtt_topic = rmodule_mqtt_topic
        self.mqtt_sender = rsender.Sender(broker, port)

        self.monitoring.send("INFO", rmodule_type, "Initializing " + rmodule_type)


    def run(self):
        while 1:
            rmodule_values = self.retrieve()
            time.sleep(0.1)


    def retrieve(self):
        retrieve_rmodule_values_request = "http://rhapsody.hestiaworkshop.net/rest/" + self.rmodule_type + "/get_values/" + self.rmodule_id
        r = requests.get(retrieve_rmodule_values_request)
        result = r.text

        if(result != self.rmodule_values):
            self.rmodule_values = result
            self.update()


    def update(self):
        # MQTT
        self.mqtt_sender.publish(self.rmodule_mqtt_topic, self.rmodule_values)
        self.monitoring.send("INFO", self.rmodule_type, "Sending update")