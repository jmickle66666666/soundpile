import tkinter as tk
from tkinter import ttk
import os
import pygame
import pathlib
from previewer import *
import assets

from PIL import Image, ImageTk

class App(ttk.Frame):
    def __init__(self, master=None, path="."):
        ttk.Frame.__init__(self, master, padding=10)

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

        # self.rebuildButton = tk.Button(self.leftside, text="rebuild", command=self.update_fileview)
        # self.rebuildButton.grid(row=1, sticky="WE")

        # self.quitButton = tk.Button(self.leftside, text="quit", command=self.quit)
        # self.quitButton.grid(row=1, column=1, sticky="WE")

        self.update_fileview()

        self.filelist.bind("<<TreeviewSelect>>", self.selection_changed)
        self.filelist.bind("<<TreeviewOpen>>", self.open)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def selection_changed(self, _):
        self.filepreview.open_file(self.filelist.focus())

    def open(self, _):
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

        dir_paths = []
        file_paths = []
        for path in os.listdir(self.path):
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


if __name__=="__main__":
    root = tk.Tk()
    root.geometry('640x480')
    root.tk.call("wm", "iconphoto", root._w, tk.PhotoImage(file="res/sound.png"))

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    pygame.mixer.init()

    app = App()
    app.master.title("SOUNDPILE")
    app.mainloop()