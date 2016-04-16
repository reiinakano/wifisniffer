# This file contains a class for spawning and killing a new dot11decrypt process
import subprocess32

class Dot11DecryptSubprocess():
    def __init__(self, interface, decryption_key):
        self.proc, self.tap = self.start_dot11decrypt(interface, decryption_key)

    def start_dot11decrypt(self, interface, decryption_key): #starts and returns dot11decrypt subprocess and interface.
        print "Starting new dot11decrypt subprocess on " + interface + " with key " + decryption_key
        proc = subprocess32.Popen(['sudo', 'd11decrypt/build/dot11decrypt', interface, decryption_key], stdout=subprocess32.PIPE)
        read = proc.stdout.readline()
        if read[0:14] == "Using device: ":
            print "Currently decrypting packets and releasing to " + read[14:].rstrip()
            print "Process number is " + str(proc.pid)
            return proc, read[14:].rstrip()
        else:
            print read
            return None, None

    def kill(self):
        print "Killing dot11decrypt subprocess and closing tap interface"
        try:
            self.proc.kill()
            subprocess32.Popen(['sudo', 'ip', 'link', 'delete', self.tap])
            print "Successfully killed this subprocess"
        except OSError as e:
            print e
            print "Oops. Can't seem to kill the process. Are you running as root?"

if __name__ == "__main__":
    dot11decryptprocess = Dot11DecryptSubprocess("wlan0", "wpa:myssid:mypassword")
    dot11decryptprocess.kill()