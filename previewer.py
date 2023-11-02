import tkinter as tk
from tkinter import ttk
import os
import pygame
import pathlib
import assets

class Previewer(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)

        self.grid()
        self.build()

    def build(self):
        self.testlabel = ttk.Label(self, text="helo there")
        self.testlabel.grid(sticky="N")

        self.image_view = tk.PhotoImage(file="res/folder.png")

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
        self.stopsound()

        filename, ext = os.path.splitext(path)

        self.image_view["file"] = ""
        self.image_label.configure(image=None)
        if assets.is_image(ext): 
            self.image_label.configure(image=self.image_view)
            self.image_view["file"] = path

        if assets.is_audio(ext):
            self.sound = pygame.mixer.Sound(path)
            self.playsound()

