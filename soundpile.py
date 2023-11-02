import tkinter as tk
from tkinter import ttk
import os
import pygame
import pathlib

from PIL import Image, ImageTk

print("hello world")

class App(tk.Frame):
    def __init__(self, master=None, path="."):
        ttk.Frame.__init__(self, master, padding=10)

        self.icon_folder = tk.PhotoImage(file="folder.png")

        self.file_icons = {}
        self.file_icons[".png"] = tk.PhotoImage(file="picture.png")

        sound_image = tk.PhotoImage(file="sound.png")
        self.file_icons[".wav"] = sound_image
        self.file_icons[".mp3"] = sound_image
        self.file_icons[".ogg"] = sound_image
        self.file_icons[".flac"] = sound_image

        self.path = path
        self.grid(sticky="NSEW")
        self.build()

    def build(self):
        self.leftside = ttk.Frame(self)
        self.leftside.grid(column = 0, row = 0, sticky="NS")
        self.leftside.rowconfigure(0, weight=1)

        self.filepreview = FileViewer(self)
        self.filepreview.grid(column=1, row = 0, sticky="NSWE")

        self.filelist = ttk.Treeview(self.leftside, show="tree")
        self.filelist.grid(columnspan=2, sticky="NS")

        self.rebuildButton = tk.Button(self.leftside, text="rebuild", command=self.update_fileview)
        self.rebuildButton.grid(row=1, sticky="WE")

        self.quitButton = tk.Button(self.leftside, text="quit", command=self.quit)
        self.quitButton.grid(row=1, column=1, sticky="WE")

        self.update_fileview()

        self.filelist.bind("<<TreeviewSelect>>", self.selection_changed)
        self.filelist.bind("<<TreeviewOpen>>", self.open)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        

    def selection_changed(self, _):
        #print("hello1!")
        #print(self.filelist.selection())
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
        print(os.listdir(self.path))

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
            if ext in self.file_icons: image = self.file_icons[ext]
            self.filelist.insert("", "end", iid=path[0], text=path[1], image=image)

class FileViewer(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)

        self.grid()
        self.build()

    def build(self):
        self.testlabel = ttk.Label(self, text="helo there")
        self.testlabel.grid(sticky="N")

        self.image_view = tk.PhotoImage(file="folder.png")

        self.image_label = ttk.Label(self, image=self.image_view)
        self.image_label.grid(sticky="N")

        self.path = ""
        self.sound = None

        self.button = ttk.Button(self, text="PLAY", command = self.playsound)
        self.button.grid(sticky="EW", row=2, column=0)

        self.button = ttk.Button(self, text="STOP", command = self.stopsound)
        self.button.grid(sticky="EW", row=2, column=1)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def playsound(self):
        if self.sound is not None: self.sound.play()

    def stopsound(self):
        if self.sound is not None: self.sound.stop()

    def open_file(self, path):
        self.path = path
        self.testlabel["text"] = path

        filename, ext = os.path.splitext(path)

        self.image_view["file"] = ""
        self.image_label.configure(image=None)
        if ext==".png": 
            self.image_label.configure(image=self.image_view)
            self.image_view["file"] = path

        if ext==".mp3":
            self.sound = pygame.mixer.Sound(path)



if __name__=="__main__":
    root = tk.Tk()
    root.geometry('640x480')

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    pygame.mixer.init()

    app = App()
    app.master.title("SOUNDPILE")
    app.mainloop()