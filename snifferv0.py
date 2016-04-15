import pyshark, time

if __name__ == '__main__':
    print("Start capture")
    capture = pyshark.LiveCapture(interface="wlan0")
    i = 1
    for packet in capture.sniff_continuously(packet_count=200):
        print '----------------Just arrived: Packet number', i
        print packet
        i+=1