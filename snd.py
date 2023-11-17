# wrapper for sound playing functions
# in case they're complicated or i need to swap libraries (again)

import winsound
import wave
import os
import assets
import ffmpeg
import math
from PIL import Image

def init():
    # pygame.mixer.init()
    pass

class Sound():
    def __init__(self, path):

        # if it is not a wav, create and cache a wav here
        _, ext = os.path.splitext(path)
        if not assets.is_wav(ext):
            ffmpeg.makeTempWAV(path)
            self.path = "temp.wav"
        else:
            self.path = path

        self.cache()
        pass

    def cache(self):
        pass
        # self.wavedata = wave.open(self.path)
        # self.total_frames = self.wavedata.getnframes()

    def play(self):
        # self.wavedata.rewind()
        # self.wavebytes = self.wavedata.readframes(self.total_frames)
        winsound.PlaySound(self.path, winsound.SND_ASYNC)
        pass

    def createWaveform(self, width, height):
        ffmpeg.makeWaveformImage(self.path, width, height)
        output = Image.open("temp.png")
        return output

    def playAt(self, perc):
        frame_position = int(self.total_frames * perc)
        self.wavedata.setpos(frame_position)
        self.wavebytes = self.wavedata.readframes(self.total_frames-frame_position)
        winsound.PlaySound(self.wavebytes, winsound.SND_ASYNC)


    def stop(self):
        winsound.PlaySound(None, 0)
        pass