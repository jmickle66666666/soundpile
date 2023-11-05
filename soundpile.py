import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import pygame
import pathlib
from previewer import *
import assets
import random

from PIL import Image, ImageTk

app=None

class App(ttk.Frame):
    def __init__(self, master=None, path="./"):
        ttk.Frame.__init__(self, master, padding=5)

        self.icon_folder = tk.PhotoImage(file="res/folder.png")
        self.icon_image = tk.PhotoImage(file="res/picture.png")
        self.icon_audio = tk.PhotoImage(file="res/sound.png")

        self.path = path
        self.grid(sticky="NSEW")
        self.build()

    def build(self):
        self.leftside = ttk.Frame(self)
        self.leftside.grid(column = 0, row = 0, sticky="NS")
        self.leftside.rowconfigure(0, weight=1)

        self.filepreview = Previewer(self)
        self.filepreview.grid(column=1, row = 0, sticky="NSWE")

        self.filelist = ttk.Treeview(self.leftside, show="tree")
        self.filelist.grid(columnspan=2, sticky="NS")
        # self.filelist.column("#0", width=0)

        self.filterArea = ttk.Frame(self.leftside)
        self.filterArea.grid(sticky="EW", row=1, columnspan=2)
        self.filterArea.columnconfigure(0, weight=1)
        self.filterArea.columnconfigure(1, weight=0)

        self.filterEntry = ttk.Entry(self.filterArea, text="APRGEHR")
        self.filterEntry.grid(sticky="EW", column=0, row=0)

        self.filterData = tk.StringVar()
        self.filterEntry["textvariable"] = self.filterData
        self.filterData.trace_add("write", self.filter_modified)

        self.filterClear = ttk.Button(self.filterArea, text="X", width=2, command=self.clear_filter)
        self.filterClear.grid(sticky="E", column=1, row=0)

        self.randomButton = ttk.Button(self.leftside, text="random??", command=self.random_sound)
        self.randomButton.grid(row=2, sticky="WE")

        self.openFolderButton = ttk.Button(self.leftside, text="open dir", command=self.open_folder)
        self.openFolderButton.grid(row=2, column=1, sticky="WE")

        self.update_fileview()

        self.filelist.bind("<<TreeviewSelect>>", self.selection_changed)
        self.filelist.bind("<<TreeviewOpen>>", self.open)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def filter_modified(self, _a=None, _b=None, _c=None):
        self.update_fileview()

    def clear_filter(self):
        self.filterData.set("")

    def random_sound(self):
        children = self.filelist.get_children()
        audios = []
        for child in children:
            filename, ext = os.path.splitext(child)
            if assets.is_audio(ext):
                audios.append(child)

        if len(audios) > 0:
            self.filelist.focus(random.choice(audios))
            self.selection_changed()
        

    def open_folder(self):
        path = tk.filedialog.askdirectory()
        self.path = path + "\\"
        self.update_fileview()

    def selection_changed(self, _=None):
        self.filepreview.open_file(self.filelist.focus())

    def open(self, _=None):
        if self.filelist.focus() == "BACK UP":
            print("ok!")
            path = pathlib.Path(self.path)
            print(path.absolute())
            print(path.absolute().parent.absolute())
            self.path = str(path.absolute().parent.absolute())+"\\"
            self.update_fileview()
        
        if os.path.isdir(self.filelist.focus()):
            self.path = self.filelist.focus() + "\\"
            self.update_fileview()

    def update_fileview(self):
        # first delete everything
        children = self.filelist.get_children()
        for child in children:
            self.filelist.delete(child)

        filter_string = self.filterData.get()

        dir_paths = []
        file_paths = []
        for path in os.listdir(self.path):
            if filter_string in path:
                if os.path.isdir(self.path + path):
                    dir_paths.append((self.path + path, path))
                else:
                    file_paths.append((self.path + path, path))

        self.filelist.insert("", "end", iid="BACK UP", text="..")

        for path in dir_paths:
            self.filelist.insert("", "end", iid=path[0], text=path[1], image=self.icon_folder)

        for path in file_paths:
            filename, ext = os.path.splitext(path[0])
            image = ""
            if assets.is_image(ext): image = self.icon_image
            if assets.is_audio(ext): image = self.icon_audio
            self.filelist.insert("", "end", iid=path[0], text=path[1], image=image)

def keyhandler(event):
    if event.keysym=="Return":
        app.open()

if __name__=="__main__":
    root = tk.Tk()
    root.geometry('640x480')
    root.tk.call("wm", "iconphoto", root._w, tk.PhotoImage(file="res/sound.png"))

    root.bind("<Key>", keyhandler)

    # ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    s = ttk.Style()
    s.theme_use('xpnative')

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    pygame.mixer.init()

    app = App()
    app.master.title("SOUNDPILE")
    app.mainloop()