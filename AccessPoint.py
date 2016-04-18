# This file contains the class for each Access Point detected by sniffer in monitor mode.
import dot11decryptprocess as d11


class AccessPoint(): # instantiating an access point checks to see if the password is saved in file 'savedAPs' and starts decryption subprocess
    def __init__(self, encryption, SSID, MAC, channel):
        self.encryption = encryption # WEP or WPA
        self.SSID = SSID # SSID of accesspoint
        self.MAC = MAC # MAC address of access point
        self.channel = channel
        self.decryptSubprocess = None
        self.openInterface = False
        self.password = self.getPasswordFromFile()
        if self.password: # if password exists
            self.startInterface() # start the interface here

    def getPasswordFromFile(self): # This method tries to get saved passkey from file and return it. returns None if failed
        try:
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
            else:
                self.decryption_key = "wep:" + self.MAC + ":" + self.password
            self.decryptSubprocess = d11.Dot11DecryptSubprocess("wlan0", self.decryption_key)
            print "Decrypting interface for " + self.SSID + " opened using passkey " + self.password
            self.openInterface = True
        except:
            print "Failed to start interface"
            pass

if __name__ == "__main__":
    AP = AccessPoint("wpa", "mySSID", "00:00:00:00:00:00")
    AP.setPasswordToFile("myPassword")
    print "Interface is open: " + str(AP.openInterface)
