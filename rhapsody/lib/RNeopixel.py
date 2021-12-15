import threading
import uuid
import json
import paho.mqtt.client as mqtt
import lib.RMonitoring as rmonitoring
import lib.NeopixelsHelper as neopixelshelper




class Neopixel(threading.Thread):
    project_id = None
    neopixel_id = None

    # MQTT
    broker = None
    port = None
    client = None
    client_id = f'rhapsody-monitoring-{uuid.uuid4()}'

    # NEOPIXELS
    neopixels_helper = None

    # MONITORING
    monitoring = None


    def on_message(self, client, userdata, received):
        instruction = json.loads(str(received.payload.decode("utf-8")))
        self.apply(instruction)


    def on_connect(self, client, userdata, flags, rc):
        if(rc == 0):
            print("Connecté à MQTT")
        else:
            print("La connection a échouée. Code %d\b")


    def __init__(self, project_id, neopixel_id, broker, port = 1883):

        threading.Thread.__init__(self)
        self.monitoring = rmonitoring.Monitoring(project_id, broker)
        self.project_id = project_id
        self.neopixel_id = neopixel_id

        self.neopixels_helper = neopixelshelper.NeopixelsHelper()

        self.broker = broker
        self.port = port

        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker, port)
        self.client.subscribe("rhapsody/christmas/" + self.neopixel_id)





    def run(self):
        while 1:
            self.client.loop()



    def apply(self, instruction):
        if(instruction['animation_name'] == "smooth_altern"):
            self.neopixels_helper.smooth_altern(int(instruction['step']), int(instruction['loop']))
        elif(instruction['animation_name'] == "smooth_altern_blue"):
            self.neopixels_helper.smooth_altern_blue(int(instruction['step']), int(instruction['loop']))
        elif(instruction['animation_name'] == "altern"):
            self.neopixels_helper.altern(int(instruction['asked_time']), int(instruction['sleep_time']), int(instruction['red_1']), int(instruction['green_1']), int(instruction['blue_1']), int(instruction['red_2']), int(instruction['green_2']), int(instruction['blue_2']))
        elif(instruction['animation_name'] == "sparkle"):
            self.neopixels_helper.sparkle(int(instruction['r']), int(instruction['g']), int(instruction['b']), int(instruction['t']))
        elif(instruction['animation_name'] == "random_sparkle"):

        elif(instruction['animation_name'] == "sparkle_with_background"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "spiral_altern_bottom_to_top"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "spiral_bottom_to_top"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "random_spiral_bottom_to_top"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "spiral_top_to_bottom"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "blink_with_color_background"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "brightness_decrease"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "multicolor_blink"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "multicolor"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "from_top_to_bottom"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "from_bottom_to_top"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "rainbow_cycle_successive"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "rainbow_cycle"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "random_from_bottom_to_top"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "flash_and_keep_old"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "random_static"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "travelling_line_bottom_to_top"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "travelling_line_top_to_bottom"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "off_all_pixels"):
            print("Not implemented yet")
        elif(instruction['animation_name'] == "set_all_pixels"):
            print("Not implemented yet")


