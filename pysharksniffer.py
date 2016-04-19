import pyshark
import threading
import AccessPoint
import CommPair


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
            # first check what kind of packet we have. Data or WLAN_MGT?
            if packet.highest_layer == "DATA": # if packet is a data packet (remember, we're only getting communicating APs)
                if self.inAPList(packet) is False: # If AP BSSID is not recognized, add it to APList. If already in list, do nothing
                    self.APlist.append(AccessPoint.AccessPoint(packet.wlan.bssid, 1))
                    print "Added new AP in APList"
                if self.inCommPairList(packet) is False:
                    self.lock.acquire()
                    self.append_new_comm_pair(packet)
                    self.lock.release()
                    print "Added new pair in CommPairList"

    def inAPList(self, packet): # checks to see if a WLAN frame's BSSID is in self.APlist
        for access_point in self.APlist:
            if access_point.MAC == packet.wlan.bssid:
                return True
        return False

    def getIndexinAPList(self, packet): # returns the index number in APList of given AP associated with packet
        for index, access_point in enumerate(self.APlist):
            if access_point.MAC == packet.wlan.bssid:
                return index
        print "Something wrong if you see this."

    def append_new_comm_pair(self, packet):
        self.index = self.getIndexinAPList(packet)
        if self.APlist[self.index].MAC == packet.wlan.sa:
            self.stn_MAC = packet.wlan.da
        elif self.APlist[self.index].MAC == packet.wlan.da:
            self.stn_MAC = packet.wlan.sa
        self.CommPairList.append(CommPair.CommunicatingPair(self.APlist[self.index], self.stn_MAC, packet.sniff_timestamp))


    def inCommPairList(self, packet): # checks to see if AP - stn pair involved in frame is already in commpairlist. if already in list, update the parameters of the pair
        for i, comm_pair in enumerate(self.CommPairList):
            if comm_pair.AP.MAC == packet.wlan.bssid and (comm_pair.stn_MAC == packet.wlan.da or comm_pair.stn_MAC == packet.wlan.sa):
                self.lock.acquire()
                self.CommPairList[i].updateTimeLastReceived(packet.sniff_timestamp)
                if comm_pair.stn_MAC == packet.wlan.da:
                    self.CommPairList[i].packet_from_AP_received()
                elif comm_pair.stn_MAC == packet.wlan.sa:
                    self.CommPairList[i].packet_to_AP_received()
                self.lock.release()
                print "Updated a pair in communicating pairs list"
                self.CommPairList[i].pretty_print()
                return True
        return False



if __name__ == "__main__":
    lock = threading.Lock()
    APlist = []
    CommPairList = []
    sniffer = PysharkMainSniffer("wlan1mon", lock, APlist, CommPairList)
    print "Thread Started"
    sniffer.start()