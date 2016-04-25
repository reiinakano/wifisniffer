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

        self.AP_listbox = Listbox(self.parent)
        for AP in self.APList:
            if AP.SSID is not None:
                self.AP_listbox.insert(END, AP.SSID)
            else:
                self.AP_listbox.insert(END, AP.MAC)
        self.AP_listbox.grid(row=1, padx=5)
        self.AP_listbox.bind("<<ListboxSelect>>", self.onSelectAP)

        self.AP_listbox_scrollbar = Scrollbar(self.parent, orient=VERTICAL)
        self.AP_listbox.config(yscrollcommand=self.AP_listbox_scrollbar.set)
        self.AP_listbox_scrollbar.config(command=self.AP_listbox.yview)
        self.AP_listbox_scrollbar.grid(row=0, column=1, rowspan=2)

    def onSelectAP(self, val):
        sender = val.widget
        index = sender.curselection()
        value = sender.get(index)
        self.AP_selected_text.set("AP: " + value)

    def updateData(self): # This method refreshes all data
        current_index = self.AP_listbox.curselection()
        print current_index
        self.AP_listbox.delete(0, END)
        for AP in self.APList:
            if AP.SSID is not None:
                self.AP_listbox.insert(END, AP.SSID)
            else:
                self.AP_listbox.insert(END, AP.MAC)
        try:
            self.AP_listbox.selection_set(current_index)
            self.AP_listbox.see(current_index)
            self.AP_listbox.selection_anchor(current_index)
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