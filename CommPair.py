# This file contains the class for instantiating a communicating pair (AP -- Station)
import AccessPoint


class CommunicatingPair():
    def __init__(self, AP, stn_MAC, time_received, channel, stn_name=None):
        self.AP = AP
        self.stn_MAC = stn_MAC
        self.time_last_received = time_received
        self.channel = channel
        self.stn_name = stn_name
        self.decrypted_packets = 0
        self.packets_from_AP = 0
        self.packets_to_AP = 0

    def deauthenticate(self): # This method deauthenticates station MAC (using aireplay-ng) in order to try to capture the EAPOL handshake
        if self.AP.openInterface == False:
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
