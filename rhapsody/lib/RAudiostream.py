import threading
import vlc
import alsaaudio
import time
import requests
import lib.RMonitoring as rmonitoring


class Audiostream(threading.Thread):

    monitoring = None

    audiostream_id = None

    audiostream_file = None
    audiostream_status = None
    audiostream_volume = None

    audio_player_instance = vlc.Instance()
    audio_player = audio_player_instance.media_player_new()
    audio_file = None
    mixer = alsaaudio.Mixer('Headphone')

    def __init__(self, audiostream_id, project_id, broker):
        threading.Thread.__init__(self)
        self.audiostream_id = audiostream_id
        self.project_id = project_id
        self.monitoring = rmonitoring.Monitoring(self.project_id, broker)


    def run(self):
        while 1:
            audiostream_values = self.get_audiostream_values()
            duration = self.audio_player.get_length() / 1000
            mm, ss = divmod(duration, 60)


            # Met à jour le status du lecteur si nécessaire
            if(audiostream_values['audiostream_status'] != self.audiostream_status):
                if(audiostream_values['audiostream_status'] == "play"):
                    self.audio_player.play()
                    self.monitoring.send("INFO", "audiostream", "playback on")
                elif(audiostream_values['audiostream_status'] == "pause"):
                    self.audio_player.pause()
                    self.monitoring.send("INFO", "audiostream", "playback off")
                self.audiostream_status = audiostream_values['audiostream_status']


            # Met à jour le fichier si nécessaire
            if(audiostream_values['audiostream_file'] != self.audiostream_file or vlc.State.Ended == self.audio_player.get_state()):
                audio_file = self.audio_player_instance.media_new("http://rhapsody.hestiaworkshop.net/files/" + audiostream_values['audiostream_file'])
                self.audio_player.set_media(audio_file)
                self.monitoring.send("INFO", "audiostream", "audio file has been changed")
                if(audiostream_values['audiostream_status'] == "play"):
                    self.audio_player.play()
                    self.monitoring.send("INFO", "audiostream", "playback on")
                self.audiostream_file = audiostream_values['audiostream_file']


            # Met à jour le volume si nécessaire
            if(audiostream_values['audiostream_volume'] != self.audiostream_volume):
                self.mixer.setvolume(int(audiostream_values['audiostream_volume']))
                self.audiostream_volume = audiostream_values['audiostream_volume']
                self.monitoring.send("INFO", "audiostream", "volume has been changed")

            time.sleep(1)


    # Récupère les valeurs des différents paramètres actuels
    # du module audiostream
    def get_audiostream_values(self):
        retrieve_audiostream_values_request = "http://rhapsody.hestiaworkshop.net/rest/audiostreams/get_values/" + self.audiostream_id
        r = requests.get(retrieve_audiostream_values_request)

        return r.json()
