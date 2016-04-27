import sys
import pyshark
import threading
import AccessPoint
import CommPair
import scapysniffer
import time


class PysharkMainSniffer(threading.Thread): # This class starts the PyShark master sniffer that updates a list of communicating APs and a list of established communications
    def __init__(self, interface_string, lock, APlist, CommPairList, intervals=True, timeout=10, sleep=10):
        threading.Thread.__init__(self)
        self.interface = interface_string
        self.lock = lock
        self.APlist = APlist
        self.CommPairList = CommPairList
        self.cap = None
        self._stop = threading.Event()
        self.intervals = intervals
        self.timeout = timeout
        self.sleep = sleep

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        self.cap = pyshark.LiveCapture(interface=self.interface)
        while True:
            try:
                if self.intervals:
                    self.cap.apply_on_packets(self.perPacket, timeout=self.timeout)
                else:
                    self.cap.apply_on_packets(self.perPacket)
            except Exception as e:
                print e
                print "Timeout"
            time.sleep(self.sleep)


    def perPacket(self, packet):
        # first check what kind of packet we have. Data or WLAN_MGT?
            if packet.highest_layer == "DATA": # if packet is a data packet (remember, we're only getting communicating APs)
                if self.inAPList(packet) is False: # If AP BSSID is not recognized, add it to APList. If already in list, do nothing
                    self.APlist.append(AccessPoint.AccessPoint(packet.wlan.bssid, 1))
                    print "Added new AP in APList"
                if self.inCommPairList(packet) is False:
                    self.lock.acquire()
                    self.append_new_comm_pair(packet)
                    self.lock.release()
            elif packet.highest_layer == "WLAN_MGT": # if packet is a wlan management packet (hopefully beacon)
                if packet.wlan.fc_subtype == "8": # this means it's a beacon frame
                    if self.inAPList(packet) is True: # If AP BSSID is recognized, try to update the AP with the SSID and encryption type
                        index = self.getIndexinAPList(packet)
                        if not self.APlist[index].SSID:
                            self.APlist[index].setName(packet.wlan_mgt.ssid)
                        if not self.APlist[index].encryption: # if encryption has not yet been set
                            self.APlist[index].setEncryption(self.getEncryption(packet))
                        #long ass condition coming up. Simply states that "if encryption and SSID are known while pass is not yet known and passfile has not yet been checked."
                        if self.APlist[index].encryption and self.APlist[index].SSID and not self.APlist[index].password and self.APlist[index].passMightBeInFile:
                            password = self.APlist[index].getPasswordFromFile()
                            if password: # if password was found in file
                                self.APlist[index].setPassword(password)  # set the password and...
                                self.APlist[index].startInterface(self.interface)  # ...start the interface
                                if self.APlist[index].openInterface:  # if opened successfully...
                                    sniffsniff = scapysniffer.ScapySniffer(self.APlist[index].decryptSubprocess.tap, self.lock, self.CommPairList)  # ...start scapy sniffer for this AP
                                    sniffsniff.start()
                            else:
                                self.APlist[index].passMightBeInFile = False
            if self.stopped():
                sys.exit()

    def getEncryption(self, packet): # takes beacon frame as input. returns the type of encryption used.
        try:
            print "Uses " + packet.wlan_mgt.rsn_pcs_list
            return "wpa"
        except Exception as e:
            print e
            print "Does not use WPA. Defaulting to WEP"
            return "wep"

    def inAPList(self, packet): # checks to see if a WLAN frame's BSSID is in self.APlist
        #c = time.clock()
        try: # this is odd, creates an error sometimes that packet.wlan.bssid is an attribute error
            localBSSID = packet.wlan.bssid # optimize
        except Exception as e:
            print packet
            print e
            sys.exit()
            # return True # ignore
        for access_point in self.APlist:
            if access_point.MAC == localBSSID:
        #        print time.clock() - c
                return True
        #print time.clock() - c
        return False

    def getIndexinAPList(self, packet): # returns the index number in APList of given AP associated with packet
        localbssid = packet.wlan.bssid
        for index, access_point in enumerate(self.APlist):
            if access_point.MAC == localbssid:
                return index
        print "Something wrong if you see this."

    def append_new_comm_pair(self, packet): # adds new commpair designated by "packet" in commpairlist
        #print packet.wlan.sa
        #print packet.wlan.da
        #print packet.wlan.ta
        #print packet.wlan.ra
        #print packet.wlan.bssid
        localwlan = packet.wlan # optimize
        index = self.getIndexinAPList(packet)
        if self.APlist[index].MAC == localwlan.sa:
            self.stn_MAC = localwlan.da
        elif self.APlist[index].MAC == localwlan.da:
            self.stn_MAC = localwlan.sa
        elif self.APlist[index].MAC == localwlan.ta:
            self.stn_MAC = localwlan.da
        elif self.APlist[index].MAC == localwlan.ra:
            self.stn_MAC = localwlan.sa
        if self.stn_MAC == "ff:ff:ff:ff:ff:ff": # if it's a broadcast frame
            return
        self.CommPairList.append(CommPair.CommunicatingPair(self.APlist[index], self.stn_MAC, packet.sniff_time))


    def inCommPairList(self, packet): # checks to see if AP - stn pair involved in frame is already in commpairlist. if already in list, update the parameters of the pair
        localbssid = packet.wlan.bssid #optimize
        localda = packet.wlan.da #optimize
        localsa = packet.wlan.sa #optimize
        for i, comm_pair in enumerate(self.CommPairList):
            if comm_pair.AP.MAC == localbssid and (comm_pair.stn_MAC == localda or comm_pair.stn_MAC == localsa):

                self.CommPairList[i].time_last_received = packet.sniff_time
                print str(packet.sniff_time)
                self.lock.acquire()
                if comm_pair.stn_MAC == localda:
                    self.CommPairList[i].packet_from_AP_received()
                else:
                    self.CommPairList[i].packet_to_AP_received()
                self.lock.release()
                #print "Updated a pair in communicating pairs list"
                #self.CommPairList[i].pretty_print()
                return True
        return False


if __name__ == "__main__":
    lock = threading.Lock()
    APlist = []
    CommPairList = []
    while True:
        sniffer = PysharkMainSniffer("wlan1mon", lock, APlist, CommPairList)
        print "Main sniffer started"
        sniffer.start()
        x = raw_input("sdadsa")
        sniffer.stop()
        sniffer.join()
        print "Main sniffer stopped"
        x = raw_input("sdasda")
