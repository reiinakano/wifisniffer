import pyshark, time, os
import dot11decryptprocess as d11

def checkPrivilege():
    print "Checking system privileges..."
    if os.getuid() == 0:
        print "Running as root."
    else:
        print "Please run program as root."
        raise Exception


if __name__ == '__main__':
    #print("Start capture")
    #capture = pyshark.LiveCapture(interface="wlan0")
    #i = 1
    #for packet in capture.sniff_continuously(packet_count=200):
    #    print '----------------Just arrived: Packet number', i
    #    print packet
    #   i+=1
    decryptProcess = d11.Dot11DecryptSubprocess("wlan0", "wpa:myssid:mypassword")
    decryptProcess.kill()
    #print proc
    #print proc.wait()
    #print proc.returncode
    #proc.kill()
