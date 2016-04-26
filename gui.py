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

        self.AP_selected_text = StringVar()
        self.AP_selected = Label(self.parent, text=0, textvariable=self.AP_selected_text)
        self.AP_selected.grid(padx=5, pady=5)

        self.AP_listbox = Listbox(self.parent, width=30)
        for AP in self.APList:
            if AP.SSID is not None:
                self.AP_listbox.insert(END, AP.SSID)
            else:
                self.AP_listbox.insert(END, AP.MAC)
        self.AP_listbox.grid(row=1, padx=5, rowspan=10)
        self.AP_listbox.bind("<<ListboxSelect>>", self.onSelectAP)

        self.AP_listbox_scrollbar = Scrollbar(self.parent, orient=VERTICAL)
        self.AP_listbox.config(yscrollcommand=self.AP_listbox_scrollbar.set)
        self.AP_listbox_scrollbar.config(command=self.AP_listbox.yview)
        self.AP_listbox_scrollbar.grid(row=1, column=1, rowspan=10, sticky = 'ns')

        self.AP_BSSID_text = StringVar()
        self.AP_BSSID = Label(self.parent, text="BSSID: ", width=30, textvariable=self.AP_BSSID_text, anchor=W)
        self.AP_BSSID.grid(row=4, column=2, padx=5, sticky=W)

        self.AP_SSID_text = StringVar()
        self.AP_SSID = Label(self.parent, text="SSID: ", width=30, textvariable=self.AP_SSID_text, anchor=W)
        self.AP_SSID.grid(row=2, column=2, padx=5, sticky=W)

        self.AP_channel_text = StringVar()
        self.AP_channel = Label(self.parent, text="Channel: ", width=30, textvariable=self.AP_channel_text, anchor=W)
        self.AP_channel.grid(row=6, column=2, padx=5, sticky=W)

        self.AP_enc_text = StringVar()
        self.AP_enc = Label(self.parent, text="Encryption: ", width=30, textvariable=self.AP_enc_text, anchor=W)
        self.AP_enc.grid(row=2, column=3, padx=5, sticky=W)

        self.AP_Pass_text = StringVar()
        self.AP_Pass = Label(self.parent, text="Password Known? ", width=30, textvariable=self.AP_Pass_text, anchor=W)
        self.AP_Pass.grid(row=4, column=3, padx=5, sticky=W)

    def onSelectAP(self, val):
        sender = val.widget
        index = sender.curselection()
        value = sender.get(index)
        self.AP_selected_text.set("AP: " + value)

        numIndex = index[0]
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