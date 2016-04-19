import pyshark
import threading
import AccessPoint


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
        for packet in self.cap.sniff_continuously(packet_count=100):
        #    # first check what kind of packet we have. Data or WLAN_MGT?
        #    if packet.highest_layer == "DATA": # if packet is a data packet (remember, we're only getting communicating APs)
        #        if self.inAPList(packet) is False: # If AP BSSID is not recognized, add it to APList. If already in list, do nothing
        #            self.APlist.append(AccessPoint.AccessPoint("wpa", packet.wlan.bssid, 1))

            if packet.highest_layer == "DATA" or packet.highest_layer == "WLAN_MGT":
                print packet.highest_layer
                try:
                    print dir(packet.wlan_mgt)
                    print packet.wlan_mgt.pretty_print()
                except:
                    pass
                print dir(packet.wlan)
                print "Receiver address: " + packet.wlan.ra
                print "Transmitter address: " + packet.wlan.ta
                print "Destination address: " + packet.wlan.da
                print "Source address: " + packet.wlan.sa
                print "BSSID: " + packet.wlan.bssid
                #print packet.wlan.pretty_print()
                print dir(packet)
                print packet.sniff_timestamp
                print packet.sniff_time
                print packet.captured_length
                print packet.layers
                print packet.interface_captured


    def inAPList(self, packet): # checks to see if a WLAN frame's BSSID is in self.APlist
        for access_point in self.APlist:
            if access_point.MAC == packet.wlan.bssid:
                return True
        return False

    def inCommPairList(self, packet):
        pass


if __name__ == "__main__":
    lock = threading.Lock()
    APlist = []
    CommPairList = []
    sniffer = PysharkMainSniffer("wlan1mon", lock, APlist, CommPairList)
    print "Thread Started"
    sniffer.start()