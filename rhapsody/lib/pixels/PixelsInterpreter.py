import json
import threading
import lib.pixels.PixelsDriver as PixelsDriver


class PixelsInterpreter(threading.Thread):

    pixelsDriver = None
    show_path = None

    def __init__(self, show_path):
        threading.Thread.__init__(self)


