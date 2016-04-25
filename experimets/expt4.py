try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
root = tk.Tk()
# use width x height + x_offset + y_offset (no spaces!)
root.geometry("240x180+130+180")
root.title('listbox with scrollbar')
# create the listbox (height/width in char)
listbox = tk.Listbox(root, width=20, height=6)
listbox.grid(row=0, column=0)
# create a vertical scrollbar to the right of the listbox
yscroll = tk.Scrollbar(command=listbox.yview, orient=tk.VERTICAL)
yscroll.grid(row=0, column=1, sticky='ns')
listbox.configure(yscrollcommand=yscroll.set)
# now load the listbox with data
friend_list = [
'Stew', 'Tom', 'Jen', 'Adam', 'Ethel', 'Barb', 'Tiny',
'Tim', 'Pete', 'Sue', 'Egon', 'Swen', 'Albert']
for item in friend_list:
    # insert each new item to the end of the listbox
    listbox.insert('end', item)
# optionally scroll to the bottom of the listbox
lines = len(friend_list)
listbox.yview_scroll(lines, 'units')
root.mainloop()