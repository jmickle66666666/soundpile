import subprocess
import os

def makeTempWAV(path):
    if os.path.exists("temp.wav"):
        os.remove("temp.wav")
    _p, ext = os.path.splitext(path)
    subprocess.run(["res/ffmpeg", "-i", path, "temp.wav"])

def makeWaveformImage(path, width, height):
    if os.path.exists("temp.png"):
        os.remove("temp.png")
    subprocess.run(["res/ffmpeg", "-i", path, "-filter_complex", "showwavespic=s="+str(width)+"x"+str(height)+":split_channels=1:colors=#ffbb00:draw=scale", "-frames:v", "1", "temp.png"])