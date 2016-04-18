import pyshark


class PysharkMainSniffer(): # This class starts the PyShark master sniffer that updates a list of communicating APs and a list of established communications
    def __init__(self, interface_string):
        self.cap = pyshark.LiveCapture(interface=interface_string)