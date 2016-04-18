import pyshark
import threading


class PysharkMainSniffer(threading.Thread): # This class starts the PyShark master sniffer that updates a list of communicating APs and a list of established communications
    def __init__(self, interface_string):
        threading.Thread.__init__(self)
        self.cap = pyshark.LiveCapture(interface=interface_string)