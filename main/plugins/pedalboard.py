import os, wave, soundfile as sf

from datetime import datetime as dt
from pedalboard import Pedalboard, Reverb
from ethon.pyfunc import bash

def slow_n_reverb(file):
    out = dt.now().isoformat("_", "seconds") + ".wav"
    bash(f'ffmpeg -i {file} {out}')
    
    # Slow down audio
    CHANNELS = 1 
    swidth = 4
    Change_RATE = 0.77
    spf = wave.open(out, 'rb')
    RATE=spf.getframerate() 
    signal = spf.readframes(-1) 
    wf = wave.open("1" + out ,'wb')
    wf.setnchannels(CHANNELS) 
    wf.setsampwidth(swidth) 
    wf.setframerate(RATE*Change_RATE) 
    wf.writeframes(signal) 
    wf.close()
    
    # Reverbing of audio
    audio, sample_rate = sf.read("1" + out)
    board = Pedalboard([Reverb(room_size=0.03)])
    effected = board(audio, sample_rate)
    sf.write("2" + out, effected, sample_rate)
    
    new_name = file.split(".")[-2] + ".mp3"
    bash(f'ffmpeg -i {"2" + out} {new_name}')  
    if os.path.isfile(file)
        os.remove(file)
    if os.path.isfile("1" + ou)
        os.remove("1" + out)
    if os.path.isfile("2" + out)
        os.remove("2" + out)
    return new_name
 
