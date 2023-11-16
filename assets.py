# various file checking utilities

types = {
    "image": [".png", ".jpg"],
    "audio": [".mp3", ".wav", ".ogg", ".flac"]
}

def is_audio(ext):
    return ext.lower() in types["audio"]

def is_image(ext):
    return ext.lower in types["image"]

def is_supported(ext):
    return is_audio(ext) or is_image(ext)