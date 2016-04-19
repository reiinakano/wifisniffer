# This file contains the class for each Access Point detected by sniffer in monitor mode.
import dot11decryptprocess as d11


class AccessPoint(): # instantiating an access point checks to see if the password is saved in file 'savedAPs' and starts decryption subprocess
    def __init__(self, MAC, channel, SSID=None, encryption=None):
        self.encryption = encryption # WEP or WPA
        self.SSID = SSID # SSID of accesspoint
        self.MAC = MAC # MAC address of access point
        self.channel = channel
        print "Instantiated AP with BSSID " + self.MAC + " at Channel " + str(self.channel)
        self.decryptSubprocess = None
        self.openInterface = False
        self.password = self.getPasswordFromFile()
        if self.password: # if password exists
            self.startInterface() # start the interface here

    def getPasswordFromFile(self): # This method tries to get saved passkey from file and return it. returns None if failed
        try:
            if self.SSID is None:
                print "SSID not known. Cannot determine password."
                return None
            print "Attempting to get AP from file 'savedAPs'..."
            f = open('savedAPs')
            for line in f.readlines():
                if ":" in line:
                    if line.split(':')[0] == self.SSID:
                        f.close()
                        print "Successfully got AP from file"
                        return line.split(':')[1].rstrip()
            print "AP not stored in file."
            f.close()
            return None

        except Exception as e:
            print e
            print "Creating file 'savedAPs'..."
            print "Newly created file has no passwords"
            f = open('savedAPs', "w")
            f.close()
            return None


    def setPasswordToFile(self, passkey): # This method writes passkey to file and sets pass for the access point
        if self.SSID is None:
            print "SSID not known. Cannot save password."
            return None
        self.password = passkey
        print "Set password to " + passkey
        print "Saving AP and password to file 'savedAPs'"
        f = open('savedAPs')
        for line in f.readlines():
                if ":" in line:
                    if line.split(':')[0] == self.SSID:
                        f.close()
                        print "AP already saved in file. Aborting."
                        return
        f.close()
        f = open('savedAPs', 'a')
        f.write(self.SSID + ":" + self.password + "\n")
        f.close()

    def startInterface(self): # start dot11decrypt subprocess
        try:
            if self.openInterface:
                print "Interface is already open. Invalid call to startInterface()"
                return
            if self.encryption == "wpa":
                self.decryption_key = "wpa:" + self.SSID + ":" + self.password
            elif self.encryption == "wep":
                self.decryption_key = "wep:" + self.MAC + ":" + self.password
            else:
                print "Encryption type not known yet. Be patient young Jedi"
                return
            self.decryptSubprocess = d11.Dot11DecryptSubprocess("wlan0", self.decryption_key)
            print "Decrypting interface for " + self.SSID + " opened using passkey " + self.password
            self.openInterface = True
        except:
            print "Failed to start interface"
            pass

    def setName(self, name):
        if name is None:
            print "Input to setName cannot be 'None'"
            return
        if self.SSID:
            print "Cannot change SSID of non-hidden network"
            return
        print "Set SSID to " + name
        self.SSID = name

    def setEncryption(self, encryption):
        print "Setting encryption to " + encryption
        self.encryption = encryption

if __name__ == "__main__":
    AP = AccessPoint("00:00:00:00:00:00", 1, "mySSID")
    AP.setEncryption("wep")
    #AP.setName("mynewSSID")
    #AP.getPasswordFromFile()
    AP.startInterface()
    print "Interface is open: " + str(AP.openInterface)
