import pyshark, time, subprocess32, os

def checkPrivilege():
    print "Checking system privileges..."
    if os.getuid() == 0:
        print "Running as root."
    else:
        print "Please run program as root."
        raise Exception


def start_dot11decrypt(interface, decryption_key): #starts and returns dot11decrypt subprocess and interface.
    print "Starting new dot11decrypt subprocess on " + interface + " with key " + decryption_key
    proc = subprocess32.Popen(['sudo', 'd11decrypt/build/dot11decrypt', interface, decryption_key], stdout=subprocess32.PIPE)
    read = proc.stdout.readline()
    if read[0:14] == "Using device: ":
        print "Currently decrypting packets and releasing to " + read[14:]
        print "Process number is " + str(proc.pid)
        return proc, read[14:]
    else:
        print read

def stop_dot11decrypt(proc, tap): #Kills tap interface
    proc.kill()

if __name__ == '__main__':
    #print("Start capture")
    #capture = pyshark.LiveCapture(interface="wlan0")
    #i = 1
    #for packet in capture.sniff_continuously(packet_count=200):
    #    print '----------------Just arrived: Packet number', i
    #    print packet
    #   i+=1
    proc, tap = start_dot11decrypt("wlan0", "wpa:myssid:mypassword")
    stop_dot11decrypt(proc, tap)
    time.sleep(1)
    #print proc
    #print proc.wait()
    #print proc.returncode
    #proc.kill()
