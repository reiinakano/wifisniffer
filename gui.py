from Tkinter import *
import AccessPoint
import pysharksniffer as pss
import threading


class MyGUI(Frame):

    def __init__(self, parent, APList, CommPairList):
        Frame.__init__(self, parent)

        self.parent = parent
        self.APList = APList
        self.CommPairList = CommPairList
        self.initUI()
        self.updateData()


    def initUI(self):

        self.parent.geometry("1200x800+100+100")
        self.parent.title("reii")
        self.init_AP_Frame()
        self.init_CommPair_Frame()


    def init_CommPair_Frame(self):
        self.CommPair_Frame = Frame(self.parent)
        self.CommPair_Frame.grid(row=1, column=0)

        self.CP_AP_selected = Label(self.CommPair_Frame, text=0, textvariable=self.AP_selected_text)
        self.CP_AP_selected.grid(padx=5, pady=5)

        self.to_label = Label(self.CommPair_Frame, text="communicating with")
        self.to_label.grid(row=1)

        self.CP_stn_selected_text = StringVar()
        self.CP_stn_selected = Label(self.CommPair_Frame, text=0, textvariable=self.CP_stn_selected_text)
        self.CP_stn_selected.grid(padx=5, pady=5, row=2)

        self.CP_listbox = Listbox(self.CommPair_Frame, width=30)
        self.CP_indexes = [] # store here the real index numbers of CommPairList corresponding to the choices in the listbox
        try:
            AP_MAC = self.APList[self.index_selected_AP].MAC
        except Exception as e:
            print e
            print "No AP selected yet"
            AP_MAC = None
        for i, CP in enumerate(self.CommPairList):
            if CP.AP.MAC == AP_MAC: # if the AP of the pair is equal to the currently selected AP, add it to the list
                self.CP_indexes.append(i)
                if CP.stn_name is not None:
                    self.CP_listbox.insert(END, CP.stn_name)
                else:
                    self.CP_listbox.insert(END, CP.stn_MAC)
        self.CP_listbox.grid(row=3, padx=5, rowspan=10)
        self.CP_listbox.bind("<<ListboxSelect>>", self.onSelectCP)

        self.CP_listbox_scrollbar = Scrollbar(self.CommPair_Frame, orient=VERTICAL)
        self.CP_listbox.config(yscrollcommand=self.CP_listbox_scrollbar.set)
        self.CP_listbox_scrollbar.config(command=self.CP_listbox.yview)
        self.CP_listbox_scrollbar.grid(row=3, column=1, rowspan=10, sticky = 'ns')

        self.CP_stn_MAC_text = StringVar()
        self.CP_stn_MAC = Label(self.CommPair_Frame, text = "Station MAC: ", width=30, textvariable=self.CP_stn_MAC_text, anchor=W)
        self.CP_stn_MAC.grid(row=4, column=2, padx=5, sticky=W)

        self.CP_stn_name_text = StringVar()
        self.CP_stn_name = Label(self.CommPair_Frame, text = "Station Name: ", width=30, textvariable=self.CP_stn_name_text, anchor=W)
        self.CP_stn_name.grid(row=6, column=2, padx=5, sticky=W)

        self.CP_time_last_received_text = StringVar()
        self.CP_time_last_received = Label(self.CommPair_Frame, text="Time of Last Comms: ", width=30, textvariable=self.CP_time_last_received_text, anchor=W)
        self.CP_time_last_received.grid(row=8, column=2, padx=5, sticky=W)

        self.CP_packets_from_AP_text = StringVar()
        self.CP_packets_from_AP = Label(self.CommPair_Frame, text="Packets from AP: ", width=30, textvariable=self.CP_packets_from_AP_text, anchor=W)
        self.CP_packets_from_AP.grid(row=10, column=2, padx=5, sticky=W)

        self.CP_packets_to_AP_text = StringVar()
        self.CP_packets_to_AP = Label(self.CommPair_Frame, text="Packets to AP:", width=30, textvariable=self.CP_packets_to_AP_text, anchor=W)
        self.CP_packets_to_AP.grid(row=12, column=2, padx=5, sticky=W)

        self.CP_decrypted_packets_text = StringVar()
        self.CP_decrypted_packets = Label(self.CommPair_Frame, text="Decrypted Packets:", width=30, textvariable=self.CP_decrypted_packets_text, anchor=W)
        self.CP_decrypted_packets.grid(row=4, column=3, padx=5, sticky=W)

        self.CP_last_decrypted_text = StringVar()
        self.CP_last_decrypted = Label(self.CommPair_Frame, text="Last Decryption:", width=30, textvariable=self.CP_last_decrypted_text, anchor=W)
        self.CP_last_decrypted.grid(row=6, column=3, padx=5, sticky=W)


    def init_AP_Frame(self):

        self.AP_Frame = Frame(self.parent)
        self.AP_Frame.grid()

        self.AP_selected_text = StringVar()
        self.AP_selected = Label(self.AP_Frame, text=0, textvariable=self.AP_selected_text)
        self.AP_selected.grid(padx=5, pady=5)

        self.AP_listbox = Listbox(self.AP_Frame, width=30)
        for AP in self.APList:
            if AP.SSID is not None:
                self.AP_listbox.insert(END, AP.SSID)
            else:
                self.AP_listbox.insert(END, AP.MAC)
        self.AP_listbox.grid(row=1, padx=5, rowspan=10)
        self.AP_listbox.bind("<<ListboxSelect>>", self.onSelectAP)

        self.AP_listbox_scrollbar = Scrollbar(self.AP_Frame, orient=VERTICAL)
        self.AP_listbox.config(yscrollcommand=self.AP_listbox_scrollbar.set)
        self.AP_listbox_scrollbar.config(command=self.AP_listbox.yview)
        self.AP_listbox_scrollbar.grid(row=1, column=1, rowspan=10, sticky = 'ns')

        self.AP_BSSID_text = StringVar()
        self.AP_BSSID = Label(self.AP_Frame, text="BSSID: ", width=30, textvariable=self.AP_BSSID_text, anchor=W)
        self.AP_BSSID.grid(row=4, column=2, padx=5, sticky=W)

        self.AP_SSID_text = StringVar()
        self.AP_SSID = Label(self.AP_Frame, text="SSID: ", width=30, textvariable=self.AP_SSID_text, anchor=W)
        self.AP_SSID.grid(row=2, column=2, padx=5, sticky=W)

        self.AP_channel_text = StringVar()
        self.AP_channel = Label(self.AP_Frame, text="Channel: ", width=30, textvariable=self.AP_channel_text, anchor=W)
        self.AP_channel.grid(row=6, column=2, padx=5, sticky=W)

        self.AP_enc_text = StringVar()
        self.AP_enc = Label(self.AP_Frame, text="Encryption: ", width=30, textvariable=self.AP_enc_text, anchor=W)
        self.AP_enc.grid(row=2, column=3, padx=5, sticky=W)

        self.AP_Pass_text = StringVar()
        self.AP_Pass = Label(self.AP_Frame, text="Password Known? ", width=30, textvariable=self.AP_Pass_text, anchor=W)
        self.AP_Pass.grid(row=4, column=3, padx=5, sticky=W)

        self.AP_Process_text = StringVar()
        self.AP_Process = Label(self.AP_Frame, text="Decrypting: ", width=30, textvariable=self.AP_Process_text, anchor=W)
        self.AP_Process.grid(row=6, column=3, padx=5, sticky=W)


    def onSelectAP(self, val):
        sender = val.widget
        index = sender.curselection()
        value = sender.get(index)
        self.AP_selected_text.set("AP: " + value)

        numIndex = index[0]
        self.index_selected_AP = numIndex

        self.updateAPDetails(numIndex)

        self.CP_listbox.delete(0, END)
        self.CP_indexes = [] # store here the real index numbers of CommPairList corresponding to the choices in the listbox
        try:
            AP_MAC = self.APList[self.index_selected_AP].MAC
        except Exception as e:
            print e
            print "No AP selected yet"
            AP_MAC = None
        for i, CP in enumerate(self.CommPairList):
            if CP.AP.MAC == AP_MAC: # if the AP of the pair is equal to the currently selected AP, add it to the list
                self.CP_indexes.append(i)
                if CP.stn_name is not None:
                    self.CP_listbox.insert(END, CP.stn_name)
                else:
                    self.CP_listbox.insert(END, CP.stn_MAC)

    def updateAPDetails(self, numIndex):
        self.AP_BSSID_text.set("BSSID: " + self.APList[numIndex].MAC)
        self.AP_channel_text.set("Channel: " + str(self.APList[numIndex].channel))

        if self.APList[numIndex].SSID is not None:
            self.AP_SSID_text.set("SSID: " + self.APList[numIndex].SSID)
        else:
            self.AP_SSID_text.set("SSID: hidden or not yet known")

        if self.APList[numIndex].encryption is not None:
            self.AP_enc_text.set("Encryption: " + self.APList[numIndex].encryption)
        else:
            self.AP_enc_text.set("Encryption: Not yet known")

        if self.APList[numIndex].password is not None:
            self.AP_Pass_text.set("Password is known")
        else:
            self.AP_Pass_text.set("Password unknown")

        if self.APList[numIndex].openInterface:
            self.AP_Process_text.set("Decrypting: Yes")
        else:
            self.AP_Process_text.set("Decrypting: No")

    def onSelectCP(self, val):
        sender = val.widget
        index = sender.curselection()
        value = sender.get(index)
        self.CP_stn_selected_text.set("Station: " + value)

        numIndex = self.CP_indexes[index[0]]
        self.updateCPDetails(numIndex)

    def updateCPDetails(self, numIndex):

        self.CP_stn_MAC_text.set("Station MAC: " + self.CommPairList[numIndex].stn_MAC)

        if self.CommPairList[numIndex].stn_name is not None:
            self.CP_stn_name_text.set("Station Name: " + self.CommPairList[numIndex].stn_name)
        else:
            self.CP_stn_name_text.set("Station Name: Not yet assigned")

        self.CP_time_last_received_text.set("Last Received: " + str(self.CommPairList[numIndex].time_last_received))

        self.CP_packets_from_AP_text.set("Packets from AP: " + str(self.CommPairList[numIndex].packets_from_AP))

        self.CP_packets_to_AP_text.set("Packets to AP: " + str(self.CommPairList[numIndex].packets_to_AP))

        self.CP_decrypted_packets_text.set("Decrypted Packets: " + str(self.CommPairList[numIndex].decrypted_packets))

        if self.CommPairList[numIndex].time_last_decrypted is not None:
            self.CP_last_decrypted_text.set("Last Decryption: " + str(self.CommPairList[numIndex].time_last_decrypted))
        else:
            self.CP_last_decrypted_text.set("Last Decryption: Never")



    def updateData(self): # This method refreshes all data
        current_index = self.AP_listbox.curselection()
        self.AP_listbox.delete(0, END)
        for AP in self.APList:
            if AP.SSID is not None:
                self.AP_listbox.insert(END, AP.SSID)
            else:
                self.AP_listbox.insert(END, AP.MAC)
        try:
            self.AP_listbox.selection_set(current_index)
            self.AP_listbox.see(current_index)
            self.AP_listbox.activate(current_index)
        except Exception as e:
            print e

        try:
            self.updateAPDetails(self.index_selected_AP)
        except Exception as e:
            print e
            print "No selected AP yet"

        current_index = self.CP_listbox.curselection()
        self.CP_listbox.delete(0, END)
        self.CP_indexes = [] # store here the real index numbers of CommPairList corresponding to the choices in the listbox
        try:
            AP_MAC = self.APList[self.index_selected_AP].MAC
        except Exception as e:
            print e
            print "No AP selected yet"
            AP_MAC = None
        for i, CP in enumerate(self.CommPairList):
            if CP.AP.MAC == AP_MAC: # if the AP of the pair is equal to the currently selected AP, add it to the list
                self.CP_indexes.append(i)
                if CP.stn_name is not None:
                    self.CP_listbox.insert(END, CP.stn_name)
                else:
                    self.CP_listbox.insert(END, CP.stn_MAC)
        try:
            self.CP_listbox.selection_set(current_index)
            self.CP_listbox.see(current_index)
            self.CP_listbox.activate(current_index)
        except Exception as e:
            print e

        try:
            self.updateCPDetails(self.CP_indexes[current_index[0]])
        except Exception as e:
            print e

        self.parent.after(1000, self.updateData)


def main():
    APList = []
    CommPairList = []
    lock = threading.Lock()
    #APList.append(AccessPoint.AccessPoint("00:00:00:00:00:00", 1))
    #APList.append(AccessPoint.AccessPoint("00:01:02:03:04:05", 2, "myssidddd"))
    sniffer = pss.PysharkMainSniffer("wlan1mon", lock, APList, CommPairList)
    print "Main sniffer started"
    sniffer.start()
    root = Tk()
    app = MyGUI(root, APList, CommPairList)
    root.mainloop()


if __name__ == '__main__':
    main()