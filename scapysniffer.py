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
        sniff(iface=self.interface_string, prn=self.perPacket, store=0)

    def perPacket(self,packet): # This method runs whenever a packet is sniffed
        print packet.summary()
        index = self.getIndexinCPList(packet)
        #if index is not None:
        #    print "huhhh"
        #    self.CommPairList[index].pretty_print()

    def getIndexinCPList(self, packet): # returns the index number in APList of given AP associated with packet
        dst = packet[Ether].dst
        src = packet[Ether].src
        for index, pair in enumerate(self.CommPairList):
            if pair.stn_MAC == dst or pair.stn_MAC == src:
                self.lock.acquire()
                self.CommPairList[index].decrypted_packet_received()
                self.lock.release()
                return index
        print "This isn't associated with a particular station"
        return None

if __name__ == "__main__":
    comm_pair_list = []
    lock = threading.Lock()
    sniffer = ScapySniffer("tap0", lock, comm_pair_list)
    sniffer.start()