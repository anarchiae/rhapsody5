import threading
import requests



class Atmosphere(threading.Thread):

    project_id = None
    current_atmosphere = None

    def __init__(self, project_id):
        threading.Thread.__init__(self)



    def run(self):
        while 1:
            print("Not implemented yet")


    def check_schedule(self):
        print("Not implemented yet")


    def retrieving_atmosphere(self):
        print("Not implemented yet")