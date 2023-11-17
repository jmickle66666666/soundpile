import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import os
import pathlib
import assets
import snd

class Previewer(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)

        self.image_view = tk.PhotoImage(file="res/logo.png")

        self.grid()
        self.build()

        self.update()
        bbox = self.grid_bbox(column=0, row=1, col2=self.grid_size()[0]-1)
        self.wsize = (bbox[2], bbox[3])

        self.bind("<Configure>", self.config_event)

    def build(self):

        # self.testlabel = ttk.Label(self, text="helo there")
        # self.testlabel.grid(sticky="N")

        self.image_label = ttk.Label(self, image=self.image_view, background="black")
        self.image_label.grid(sticky="NSEW", columnspan=2, row=0)

        self.path = ""
        self.sound = None

        self.transportArea = ttk.Frame(self)
        self.transportArea.grid(row=1, columnspan=2)

        self.transportArea.columnconfigure(0, weight=1)
        self.transportArea.columnconfigure(1, weight=1)

        self.button = ttk.Button(self.transportArea, text="PLAY", command = self.playsound)
        self.button.grid(sticky="EW", row=0, column=0)

        self.button = ttk.Button(self.transportArea, text="STOP", command = self.stopsound)
        self.button.grid(sticky="EW", row=0, column=1)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def playsound(self):
        if self.sound is not None: 
            self.sound.play()

    def stopsound(self):
        if self.sound is not None: self.sound.stop()

    def wave_preview(self, width, height):
        if self.sound is not None: 
            img = self.sound.createWaveform(width, height)
            self.image_view["file"] = "temp.png"
            self.image_label.configure(image=self.image_view)

    def config_event(self, e):
        bbox = self.grid_bbox(column=0, row=0, col2=self.grid_size()[0]-1)
        wsize = (bbox[2], bbox[3])
        if wsize[0] != self.wsize[0] or wsize[1] != self.wsize[1]:
            self.wsize = wsize
            self.wave_preview(wsize[0], wsize[1])

    def open_file(self, path):
        self.path = path
        # self.testlabel["text"] = path
        self.stopsound()

        filename, ext = os.path.splitext(path)

        #self.image_view["file"] = ""
        #self.image_label.configure(image=None)
        # if assets.is_image(ext): 
        #     self.image_label.configure(image=self.image_view)
        #     self.image_view["file"] = path

        if assets.is_audio(ext):
            self.sound = snd.Sound(path)
            self.playsound()

            self.update()
            bbox = self.grid_bbox(column=0, row=0, col2=self.grid_size()[0]-1)
            self.wave_preview(bbox[2], bbox[3])


