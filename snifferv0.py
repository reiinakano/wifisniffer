import pyshark, time, subprocess32

if __name__ == '__main__':
    #print("Start capture")
    #capture = pyshark.LiveCapture(interface="wlan0")
    #i = 1
    #for packet in capture.sniff_continuously(packet_count=200):
    #    print '----------------Just arrived: Packet number', i
    #    print packet
    #   i+=1
    proc = subprocess32.Popen(['d11decrypt/build/dot11decrypt', 'wlan0', 'wpa:thisismyssid:thisismypass'])
    time.sleep(1)
    print proc.poll()
    print proc.returncode