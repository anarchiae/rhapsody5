import requests
import lib.RModule as rmodule
import lib.RAudiostream as raudiostream
import lib.RAtmosphere as ratmosphere
import lib.RMonitoring as rmonitoring



class Project:
    project_id = None

    switchboards = []
    neopixels = []

    audiostream = None
    monitoring = None

    def __init__(self, project_id, broker):
        self.project_id = project_id

        # STARTING MONITORING SERVICE
        self.monitoring = rmonitoring.Monitoring(self.project_id, broker)

        # LOADING SWITCHBOARDS
        retrieve_switchboards_request = "http://rhapsody.hestiaworkshop.net/rest/switchboards/get_switchboards/" + self.project_id
        try:
            r =  requests.get(retrieve_switchboards_request)
            result = r.json()
            for switchboard in result:
                new_switchboard = rmodule.Module("switchboards", switchboard['switchboard_id'], switchboard['switchboard_mqtt_topic'], project_id, broker)
                self.switchboards.append(new_switchboard)
        except Exception as e:
            self.monitoring.send("ERROR", "project_initialization -> while loading switchboards", str(e))

        # LOADING  NEOPIXELS
        retrieve_neopixels_request = "http://rhapsody.hestiaworkshop.net/rest/neopixels/get_neopixels/" + self.project_id
        try:
            r = requests.get(retrieve_neopixels_request)
            result = r.json()
            for neopixel in result:
                new_neopixel = rmodule.Module("neopixels", neopixel['neopixel_id'], neopixel['neopixel_mqtt_topic'], project_id, broker)
                self.neopixels.append(new_neopixel)
        except:
            self.monitoring.send("ERROR", "project_initialization -> while loading neopixels", str(e))


        # MODULES
        # LOADING AUDIOSTREAM MODULE
        try:
            self.audiostream = raudiostream.Audiostream("13041983", self.project_id, broker)
        except Exception as e:
            self.monitoring.send("ERROR", "project_initialization -> while loading audiostream module", str(e))

        # LOADING NEOPIXEL MODULE
        try:
            self.neopixel = rneopixel.Neopixel("01101974", self.project_id, broker)
        except Exception as e:
            self.monitoring.send("ERROR", "project_initialization -> while loading neopixel module", str(e))


        # SERVICES
        # LOADING ATMOSPHERES SERVICE
        #atmosphere = ratmosphere.Atmosphere(self.project_id)




    def begin(self):
        # mlmkl
        try:
            for switchboard in self.switchboards:
                switchboard.start()
        except Exception as e:
            self.monitoring.send("ERROR", "starting_project -> starting switchboards", str(e))

        # Starts neopixel modules
        try:
            for neopixel in self.neopixels:
                neopixel.start()
        except Exception as e:
            self.monitoring.send("ERROR", "starting_project -> starting neopixels", str(e))


        # Starts audiostream module
        try:
            self.audiostream.start()
        except Exception as e:
            self.monitoring.send("starting_project -> starting audiostream", str(e))
