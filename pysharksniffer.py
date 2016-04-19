import pyshark
import threading


class PysharkMainSniffer(threading.Thread): # This class starts the PyShark master sniffer that updates a list of communicating APs and a list of established communications
    def __init__(self, interface_string, lock, APlist, CommPairList):
        threading.Thread.__init__(self)
        self.interface = interface_string
        self. lock = lock
        self.APlist = APlist
        self.CommPairList = CommPairList
        self.cap = None

    def run(self):
        self.cap = pyshark.LiveCapture(interface=self.interface)
        for packet in self.cap.sniff_continuously(packet_count=10):
            print dir(packet)
            packet.pretty_print()
            pass

if __name__ == "__main__":
    lock = threading.Lock()
    APlist = []
    CommPairList = []
    sniffer = PysharkMainSniffer("wlan1mon", lock, APlist, CommPairList)
    print "Thread Started"
    sniffer.start()