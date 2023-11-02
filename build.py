import PyInstaller.__main__
import shutil
import os

if os.path.exists("dist"):
    shutil.rmtree("dist")

if os.path.exists("soundpile.zip"):
    os.remove("soundpile.zip")

PyInstaller.__main__.run([
    'soundpile.py',
    '--onefile',
    '--noconsole',
    '-ires/icon.png'
])

shutil.copytree("res", "dist/res")

shutil.make_archive("soundpile", "zip", "dist")