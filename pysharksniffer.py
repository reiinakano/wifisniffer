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
        for packet in self.cap.sniff_continuously(packet_count=100000):
            # first check what kind of packet we have. Data or WLAN_MGT?
            if packet.highest_layer == "DATA": # if packet is a data packet (remember, we're only getting communicating APs)
                if self.inAPList(packet) is False: # If AP BSSID is not recognized, add it to APList. If already in list, do nothing
                    self.APlist.append(AccessPoint.AccessPoint(packet.wlan.bssid, 11))
                    print "Added new AP in APList"
                if self.inCommPairList(packet) is False:
                    self.lock.acquire()
                    self.append_new_comm_pair(packet)
                    self.lock.release()
                    print "Added new pair in CommPairList"
            if packet.highest_layer == "WLAN_MGT": # if packet is a wlan management packet (hopefully beacon)
                if packet.wlan.fc_subtype == "8": # this means it's a beacon frame
                    if self.inAPList(packet) is True: # If AP BSSID is recognized, try to update the AP with the SSID and encryption type
                        self.index = self.getIndexinAPList(packet)
                        if not self.APlist[self.index].SSID:
                            self.APlist[self.index].setName(packet.wlan_mgt.ssid)
                        if not self.APlist[self.index].encryption: # if encryption has not yet been set
                            self.APlist[self.index].setEncryption(self.getEncryption(packet))
                        #long ass condition coming up. Simply states that "if encryption and SSID are known while pass is not yet known and passfile has not yet been checked."
                        if self.APlist[self.index].encryption and self.APlist[self.index].SSID and not self.APlist[self.index].password and self.APlist[self.index].passMightBeInFile:
                            password = self.APlist[self.index].getPasswordFromFile()
                            if password: # if password was found in file
                                self.APlist[self.index].setPassword(password) # set the password and
                                self.APlist[self.index].startInterface("wlan1mon") # start the interface
                            else:
                                self.APlist[self.index].passMightBeInFile = False

    def getEncryption(self, packet): # takes beacon frame as input. returns the type of encryption used.
        try:
            print "Uses " + packet.wlan_mgt.rsn_pcs_list
            return "wpa"
        except Exception as e:
            print e
            print "Does not use WPA. Defaulting to WEP"
            return "wep"

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

    def append_new_comm_pair(self, packet): # adds new commpair designated by "packet" in commpairlist
        #print packet.wlan.sa
        #print packet.wlan.da
        #print packet.wlan.ta
        #print packet.wlan.ra
        #print packet.wlan.bssid
        self.index = self.getIndexinAPList(packet)
        if self.APlist[self.index].MAC == packet.wlan.sa:
            self.stn_MAC = packet.wlan.da
        elif self.APlist[self.index].MAC == packet.wlan.da:
            self.stn_MAC = packet.wlan.sa
        elif self.APlist[self.index].MAC == packet.wlan.ta:
            self.stn_MAC = packet.wlan.da
        elif self.APlist[self.index].MAC == packet.wlan.ra:
            self.stn_MAC = packet.wlan.sa
        self.CommPairList.append(CommPair.CommunicatingPair(self.APlist[self.index], self.stn_MAC, packet.sniff_timestamp))


    def inCommPairList(self, packet): # checks to see if AP - stn pair involved in frame is already in commpairlist. if already in list, update the parameters of the pair
        for i, comm_pair in enumerate(self.CommPairList):
            if comm_pair.AP.MAC == packet.wlan.bssid and (comm_pair.stn_MAC == packet.wlan.da or comm_pair.stn_MAC == packet.wlan.sa):
                self.lock.acquire()
                self.CommPairList[i].updateTimeLastReceived(packet.sniff_time)
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