# wifisniffer

This program aims to capture all the WiFi signals floating around and decrypt individual packets using well-known methods.

First step is to identify all communicating access points and stations using Pyshark.

After identifying the type of encryption used by the communicating pairs, we use the dot11decrypt library to decode them and start a new tap interface outputting the decoded packets.

These decoded packets are then parsed using Scapy. After this, we are free to get whatever information we need from the packets. One thing I do here is get the DNS requests from each station and display them in a (rather ugly and poorly coded) GUI.
