# This file contains the class for instantiating a communicating pair (AP -- Station)
import AccessPoint as AP


class CommunicatingPair():
    def __init__(self, AP, stn_MAC, time_received, stn_name=None):
        self.AP = AP
        self.stn_MAC = stn_MAC
        self.time_last_received = time_received
        self.channel = self.AP.channel
        self.stn_name = stn_name
        self.decrypted_packets = 0
        self.packets_from_AP = 0
        self.packets_to_AP = 0
        print "Instantiated communicating pair with AP MAC " + self.AP.MAC + " and station MAC " + self.stn_MAC

    def deauthenticate(self): # This method deauthenticates station MAC (using aireplay-ng) in order to try to capture the EAPOL handshake
        if self.AP.openInterface is False:
            print "There is no dot11decrypt process listening for this access point. Deauthenticating is pointless."
            return
        else:
            # do deauthentication here
            print "Deauthentication packets sent"
            pass

    def setName(self, name): # This method allows user to set name of the station e.g. AdminPC
        self.stn_name = name
        print "Set name of " + self.stn_MAC + " to " + self.stn_name

    def updateTimeLastReceived(self, time_received):
        self.time_last_received = time_received

    def packet_from_AP_received(self):
        self.packets_from_AP += 1

    def packet_to_AP_received(self):
        self.packets_to_AP += 1

    def decrypted_packet_received(self):
        self.decrypted_packets += 1
        print self.decrypted_packets

    def pretty_print(self):
        print "Communicating pair with AP MAC " + self.AP.MAC + " and station MAC " + self.stn_MAC
        print "Time last received: " + str(self.time_last_received)
        print "Packets from AP: " + str(self.packets_from_AP)
        print "Packets to AP:" + str(self.packets_to_AP)

if __name__ == '__main__':
    access_point = AP.AccessPoint("wpa", "mySSID2", "10:20:30:40:50:60", 1)
    access_point.setPasswordToFile("mypassword2")
    access_point.startInterface()
    access_point.startInterface()
    CommPair = CommunicatingPair(access_point, "00:01:02:03:04:05", 42)
    CommPair.deauthenticate()
    CommPair.setName("AdminPC")
    print CommPair.stn_name