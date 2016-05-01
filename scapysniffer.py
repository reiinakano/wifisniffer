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

    def perPacket(self, packet): # This method runs whenever a packet is sniffed
        print packet.summary()
        index = self.getIndexinCPList(packet)
        if index is not None:
            self.talked_to_address(packet, index)
            self.DNSquery(packet, index)
        #    self.CommPairList[index].pretty_print()

    def getIndexinCPList(self, packet): # returns the index number in APList of given AP associated with packet
        dst = packet[Ether].dst
        src = packet[Ether].src
        for index, pair in enumerate(self.CommPairList):
            if pair.stn_MAC == dst or pair.stn_MAC == src:
                self.lock.acquire()
                self.CommPairList[index].decrypted_packet_received()
                self.lock.release()
                self.CommPairList[index].time_last_decrypted = packet.time
                print packet.time
                return index
        print "This isn't associated with a particular station"
        return None

    def talked_to_address(self, packet, index): # This function stores a node (IP+port) that the commpair talked to.
        ip = None
        dport = None
        proto = None
        if packet.haslayer(IP):
            ip = packet[IP].dst
        if packet.haslayer(TCP):
            dport = packet[TCP].dport
            proto = "TCP"
        elif packet.haslayer(UDP):
            dport = packet[UDP].dport
            proto = "UDP"
        toAppend = (ip, dport, proto)
        self.CommPairList[index].IP_addresses_and_ports_talked_to.add(toAppend)
        #print self.CommPairList[index].IP_addresses_and_ports_talked_to

    def DNSquery(self, packet, index):
        if packet.haslayer(DNSQR):
            if packet[DNSQR].qname not in self.CommPairList[index].DNS_queries:
                self.CommPairList[index].DNS_queries.append(packet[DNSQR].qname)
            print self.CommPairList[index].DNS_queries


if __name__ == "__main__":
    comm_pair_list = []
    lock = threading.Lock()
    sniffer = ScapySniffer("tap0", lock, comm_pair_list)
    sniffer.start()