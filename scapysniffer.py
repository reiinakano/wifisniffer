from scapy.all import *
import threading

# This class starts a scapy sniffer assigned to a tap interface and updates a given list of communicating pairs.
# Any packet it receives will go into updating the data of the particular communicating pair the packet is associated
# with.
class ScapySniffer(threading.Thread):
    def __init__(self, interface_string, lock, CommPairList):
        threading.Thread.__init__(self)
        self.interface_string = interface_string
        self.lock = lock
        self.CommPairList = CommPairList

    def run(self):
        sniff(prn=self.perPacket, store=0)

    def perPacket(self,packet): # This method runs whenever a packet is sniffed
        print packet.summary()

if __name__ == "__main__":
    comm_pair_list = []
    lock = threading.Lock()
    sniffer = ScapySniffer("wlan0", lock, comm_pair_list)
    sniffer.start()