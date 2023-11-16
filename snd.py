# wrapper for sound playing functions
# in case they're complicated or i need to swap libraries (again)

# import pygame
import winsound
import wave

def init():
    # pygame.mixer.init()
    pass

class Sound():
    def __init__(self, path):
        self.path = path
        self.cache()
        # if it is not a wav, create and cache a wav here
        pass

    def cache(self):
        self.wavedata = wave.open(self.path)
        self.total_frames = self.wavedata.getnframes()

    def play(self):
        self.wavedata.rewind()
        self.wavebytes = self.wavedata.readframes(self.total_frames)
        winsound.PlaySound(self.wavebytes, winsound.SND_MEMORY )
        pass

    def playAt(self, perc):
        frame_position = int(self.total_frames * perc)
        self.wavedata.setpos(frame_position)
        self.wavebytes = self.wavedata.readframes(self.total_frames-frame_position)
        winsound.PlaySound(self.wavebytes, winsound.SND_ASYNC)


    def stop(self):
        winsound.PlaySound(None, 0)
        pass