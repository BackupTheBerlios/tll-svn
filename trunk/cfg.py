#!/usr/bin/env python

from Tkinter import *
from tkFileDialog import askopenfilename, askdirectory
import launch
load_config, config_files = launch.load_config, launch.config_files

ALIASES, HISTORY = load_config(*config_files())

def set_entry(entry, value):
    entry.delete(0, END)
    entry.insert(0, value)


class ConfigDlg:
    def __init__(self, parent):
        self._top = Toplevel(parent)
        left = Frame(self._top)
        #Label(left, text="Alias:", anchor=W).pack(anchor=W)
        sb = Scrollbar(left, orient=VERTICAL)
        self._lb = Listbox(left, selectmode=SINGLE, yscrollcommand=sb.set)
        sb.config(command=self._lb.yview)
        aliases = ALIASES.keys()
        aliases.sort()
        for alias in aliases:
            self._lb.insert(END, alias)
        self._lb.bind("<Button-1>", self.on_list)
        self._lb.pack(side=LEFT, fill=BOTH, expand=1)
        sb.pack(side=RIGHT, fill=Y, expand=1)
        left.pack(side=LEFT, expand=1, fill=BOTH)
        right = Frame(self._top)
        self._alias = self.add_field(right, "Alias:")
        self._filename = self.add_field(right, "Filename:", self.get_filename)
        self._arguments = self.add_field(right, "Arguments:")
        self._directory = self.add_field(right, "Directory:", self.get_dirname)
        #f = Frame(self._top)
        self.add_button(right, "Add")
        self.add_button(right, "Update")
        self.add_button(right, "Delete")
        b = Button(right, width=10, text="Quit", 
                   command=lambda: self._top.destroy())
        b.pack(side=RIGHT)
        #self.add_button(right, "Quit", lambda: self._top.destroy())
        right.pack(side=LEFT, expand=1, anchor=N, fill=BOTH)
        #f.pack(expand=1)

        # Activate first item
        if aliases:
            e = Event()
            e.widget = self._lb
            e.y = 0
            self.on_list(e)
            self._lb.select_set(0)

    def on_list(self, e):
        w = e.widget
        i = w.nearest(e.y)
        alias = w.get(i)

        app = ALIASES[alias]
        set_entry(self._alias, alias)
        set_entry(self._filename, app.filename)
        set_entry(self._arguments, " ".join(app.arguments))
        set_entry(self._directory, app.directory)

    def get_filename(self):
        fname = askopenfilename()
        if fname:
            set_entry(self._filename, fname)

    def get_dirname(self):
        dirname = askdirectory()
        if dirname:
            set_entry(self._directory, dirname)

    def add_button(self, parent, text, command=None):
        if command:
            b = Button(parent, text=text, width=10, command=command)
        else:
            b = Button(parent, text=text, width=10)

        b.pack(side=LEFT, anchor=S)

    def add_field(self, parent, name, button_cmd = None):
        f = Frame(parent)
        Label(f, text=name, width=10, anchor=W).pack(side=LEFT)
        e = Entry(f, width=60)
        e.pack(side=LEFT, expand=1, pady=5, fill=X)
        if button_cmd:
            Button(f, text="...", command=button_cmd).pack(pady=5)
        f.pack(anchor=NW, expand=1, fill=X)

        return e

    def on_up(self, e):
        print "UP"

    def on_down(self, e):
        print "DOWN"

if __name__ == "__main__":
    root = Tk()
    d = ConfigDlg(root)
    d._top.lift()
    root.wait_window(d._top)
