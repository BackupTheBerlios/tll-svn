#!/usr/bin/env python
'''Lanuch applications with aliases.
Modeled after SlickRun utility.
'''

# =====================================================
# Copyright (c) Miki Tebeka <miki.tebeka@zoran.com> 
# This file is under the GNU Public License (GPL), see
# http://www.gnu.org/copyleft/gpl.html for more details
# =====================================================

__author__ = "Miki Tebeka <miki.tebeka@zoran.com>"
# $Id: launch.pyw 1033 2004-12-30 15:07:07Z mikit $

# Imports
from os.path import isfile, dirname, join
from os import environ, chdir
from ConfigParser import ConfigParser, Error as ConfigParserError
from sys import path, platform, stderr
import sys
from glob import glob
from user import home
from shlex import split
import re
from sets import Set
if platform == "win32":
    from os import startfile
else:
    WindowsError = OSError
from os import P_NOWAIT
try:
    from os import spawnvp as spawn
except ImportError:
    from os import spawnv as spawn
from Tkinter import *
from tkMessageBox import showerror, showinfo
from tkFileDialog import askopenfilename, askdirectory

class ConfigDlg:
    '''Edit configuration'''
    def __init__(self, parent):
        self._top = Toplevel(parent)
        left = Frame(self._top)
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
        self.add_button(right, "Add")
        self.add_button(right, "Update")
        self.add_button(right, "Delete")
        b = Button(right, width=10, text="Quit", 
                   command=self._top.destroy)
        b.pack(side=RIGHT)
        right.pack(side=LEFT, expand=1, anchor=N, fill=BOTH)

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

def set_entry(entry, value):
    entry.delete(0, END)
    entry.insert(0, value)

class App:
    '''Application datat type'''
    def __init__(self, filename, arguments, directory):
        self.filename = filename
        self.arguments = arguments
        self.directory = directory

# List of aliases
ALIASES = {}

def appdir():
    '''Application directory'''
    appdir = path[0]
    if isfile(appdir): # py2exe
        return dirname(appdir)
    return appdir

def show_help():
    '''Show the help'''
    readme = join(appdir(), "Readme.txt")
    if not isfile(readme):
        showerror("Missing Help", "Can't find help file %s" % readme)
        return

    showinfo("Little Launcher Help", open(readme, "rt").read())

import cfg
def show_setup():
    '''Show the setup dialog'''
    # FIXME: Not implemented
    conf, hist = config_files()
    d = cfg.ConfigDlg(root)
    #showinfo("Manual Setup Currently", "Please edit %s manually" % cfg)

def fix_cmd(cmd):
    '''Fix command for shlex'''
    return cmd.replace("\\", "/")

# FIXME: In cygwin environment we might want to try "cygstart" as well
def run(str):
    '''Run an application'''
    fields = split(fix_cmd(str))
    cmd = fields.pop(0).lower()
    if cmd == "help":
        show_help()
        return 0
    if cmd == "setup":
        show_setup()
        return 0

    # UNC file name fixing
    if (platform == "win32") and cmd.startswith("//"):
        cmd = cmd.replace("/", "\\")

    # Find if we have an alias
    dirname = ""
    if cmd in ALIASES:
        app = ALIASES[cmd]
        cmd = app.filename
        fields = app.arguments + fields
        dirname = app.directory

    # Fix environment from py2exe
    if hasattr(sys, "frozen"):
        for key in ("TCL_LIBRARY", "TK_LIBRARY"):
            if key in environ:
                del environ[key]
    # Run
    try:
        if dirname:
            dirname = dirname.replace("\\", "/")
            chdir(dirname)
        if (not fields) and (platform == "win32"):
            startfile(cmd)
            return 1
        else:
            spawn(P_NOWAIT, cmd, [cmd] + fields)
            return 1
    except (OSError, WindowsError), e:
        showerror("Execution Error", "%s" % e.strerror)
        return 0

# Config file name
def config_files():
    '''Name of configuration files'''
    base = "launchrc"
    hist = "launch_history"
    if platform == "win32":
        pre = "_"
    else:
        pre = "."
    cfg = join(home, pre + base)
    if isfile(cfg):
        return cfg, join(home, pre + "hist")
    cfg = join(appdir(), pre + base)
    if isfile(cfg):
        return cfg, join(appdir(), pre + hist)
    raise IOError("can't find config file")

def load_config(cfgfile, histfile):
    '''Load config file'''
    cp = ConfigParser()
    cp.readfp(open(cfgfile))
    aliases = {}
    for sect in cp.sections():
        fname = cp.get(sect, "filename")
        if cp.has_option(sect, "arguments"):
            args = split(fix_cmd(cp.get(sect, "arguments")))
        else:
            args = []
        if cp.has_option(sect, "directory"):
            dirname = cp.get(sect, "directory")
        else:
            dirname = ""
        aliases[sect.lower()] = App(fname, args, dirname)

    history = []
    try:
        for line in open(histfile):
            line = line.strip()
            if line:
                history.append(line)
    except IOError: # Ignore errors in history file
        pass

    return aliases, history

# GUI Settings
fg = "green"
bg = "black"
font = ("Courier", 14)

class Matcher:
    '''Find possible matches for current typed prefix'''
    def __init__(self, history, aliases):
        '''Set history and aliases'''
        self.history = history
        self.aliases = aliases

    def get_matches(self, prefix, get_files = 1):
        '''Get all matches for "prefix"'''
        pre = prefix.lower()

        hist = [h for h in self.history if h.lower().startswith(pre)]
        als = [a for a in self.aliases if a.lower().startswith(pre)]
        als = [a for a in als if a not in hist]
        
        sys = [s for s in ("setup", "help") if s.lower().startswith(pre)]

        if not get_files:
            return hist + als + sys

        # Get matching files
        files = Set(glob(pre + "*"))
        fields = pre.split()
        for i, f in enumerate(fields):
            for path in glob(f + "*"):
                files.update([" ".join(fields[:i] + [path])])

        return hist + als + sys + list(files)

    def selected(self, item):
        '''Notified the item was selected, add it to history'''
        if item in self.history:
            self.history.remove(item)
        self.history.insert(0, item)

class Completer(Frame):
    '''Main GUI class'''
    def __init__(self, root, matcher, *args, **kw):
        Frame.__init__(self, root, *args, **kw)

        # Text entry
        self._entry = Entry(root, width=50, font=font, fg=fg, bg=bg)
        self._entry.pack(fill=X, side=LEFT, expand=1)

        # Bind keys
        self._entry.bind("<Escape>", self.on_quit)
        self._entry.bind("<Return>", self.on_cmd)
        self._entry.bind("<Up>", self.on_updown)
        self._entry.bind("<Down>", self.on_updown)
        self._entry.bind("<FocusIn>", lambda e: self.kill_pop())
        # Combo like button
        b = Button(self, text="v", command=self.show_all)
        b.pack(side=RIGHT)

        self._entry.focus()
        self.root = root # Store root

        self.poplist = None # Current poplist
        self.matcher = matcher # Matcher object
        self.prev = "" # Previous value

        self.poll() # Poll changes in _entry

    def show_all(self):
        '''Show all possible items in history + aliases'''
        if self.poplist:
            self.poplist.destroy()
            self.poplist = None
        matches = self.matcher.get_matches("", 0)
        self.poplist = Poplist(matches, self.set_entry)

    def kill_pop(self):
        '''Kill current pop window'''
        if self.poplist:
            self.poplist.destroy()
            self.poplist = None

    def set_entry(self, value):
        '''Set entry value'''
        self.prev = value
        self._entry.delete(0, END)
        self._entry.insert(0, value)

    def on_updown(self, e):
        '''Handle UP/DOWN arrows'''
        if self.poplist:
            self.poplist.focus()
        else:
            self.show_all()

    def poll(self):
        '''Poll entry widget for changes'''
        def check():
            '''Check functions'''
            # We use this function so that no matter where we exit we'll call
            # self.after at the end
            if self._entry.focus_get() != self._entry:
                return
            val = self._entry.get()
            if val == self.prev:
                return
            self.prev = val
            self.kill_pop()
            matches = self.matcher.get_matches(val)
            if not matches:
                return
            self.poplist = Poplist(matches, self.set_entry)
            self._entry.focus()
        check()
        self.after(100, self.poll)
            
    def on_quit(self, e):
        '''ESC = quit program'''
        self.root.quit()

    def on_cmd(self, e):
        '''Enter = run command'''
        cmd = self._entry.get()
        if run(cmd):
            self.matcher.selected(cmd)
            self.quit()


class Poplist(Toplevel):
    '''Show all possible matches'''
    def __init__(self, items, setval):
        # Create new window
        Toplevel.__init__(self, root)
        self.setval = setval
        # List box with items
        self._list = lb = Listbox(self, width=50, font=font, fg=fg, bg=bg)
        for item in items:
            lb.insert(END, item)
        # Select 1'st item
        lb.select_set(0)
        lb.activate(0)
        lb.pack(fill=BOTH, expand=1)
        # Bind Double click, Enter and ESC keys
        lb.bind("<Escape>", lambda e: self.destroy())
        lb.bind("<FocusOut>", lambda e: self.destroy())
        lb.bind("<Return>", self.on_enter)
        lb.bind("<Double-Button-1>", self.on_enter)

        self.focus = lb.focus

        # Set popup like window
        self.transient(root)
        self.overrideredirect(1) # No borders
        root.update_idletasks() # Make "geometry" work

        # FIXME: Find a better placement algorithm
        w = self.winfo_width()
        h = self.winfo_height()
        fields = root.geometry().split("+")
        rx = int(fields[1])
        ry = int(fields[2])
        rw, rh = [int(i) for i in fields[0].split("x")]
        self.geometry("%dx%d+%d+%d" % (w, h, rx + rw - w - 10, ry + rh + 20))
        self.poll()

    def on_enter(self, e):
        '''Enter event handler'''
        lb = e.widget
        line = lb.get(ACTIVE)
        self.setval(line)
        self.destroy()

    def poll(self):
        '''Poll on changes in listbox'''
        if self.focus_get() == self._list:
            self.setval(self._list.get(ACTIVE))
        self.after(100, self.poll)

def center_on_screen(root):
    '''Center window on screen'''
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    w = root.winfo_width()
    sh = root.winfo_screenheight()
    h = root.winfo_height()
    root.geometry("%dx%d+%d+%d" % (w, h, sw/2 - w/2, sh/2 - h/2 - 100))

if __name__ == "__main__":
    from sys import platform
    from optparse import OptionParser

    oparser = OptionParser("usage: %prog [options]",
            version="%prog 0.2.0")
    oparser.add_option("-m", "--max-hist", help="maximal size of history",
            dest="histsize", default=200, type="int")

    opts, args = oparser.parse_args()
    if args:
        oparser.error("wrong number of arguments") # Will exit


    root = Tk() # Root window

    # Load config files
    try:
        cfgfile, histfile = config_files()
        ALIASES, history = load_config(cfgfile, histfile)
    except (IOError, ConfigParserError), e:
        showerror("Config file Error", "%s" % e)
        raise SystemExit(1)
    
    if len(history) > opts.histsize:
        history = history[:histsize]

    if platform in ("cygwin", "win32"): # Avoid flicker on win32
        root.withdraw() # Show only after positioning
    root.title("The Little Launcher")
    root.resizable(width=1, height=0) # Resize on width
    m = Matcher(history, ALIASES)
    _cmd = Completer(root, m, width=1, height=0)
    _cmd.pack(fill=X, expand=1)
    center_on_screen(root)
    root.deiconify()


    # Run GUI
    root.mainloop()

    # Save history
    try:
        fo = open(histfile, "wt")
        for item in history:
            print >> fo, item
    except IOError:
        raise SystemExit("can't save history to %s" % histfile)
