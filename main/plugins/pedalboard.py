import os, wave, soundfile as sf

from datetime import datetime as dt
from pedalboard import Pedalboard, Reverb
from ethon.pyfunc import bash

def slow_n_reverb(file):
    mp3 = dt.now().isoformat("_", "seconds") + ".mp3"
    out = dt.now().isoformat("_", "seconds") + ".wav"
    os.rename(file, mp3)
    bash(f'ffmpeg -i {mp3} {out} -y')
    
    # Slow down audio
    CHANNELS = 1 
    swidth = 4
    Change_RATE = 0.83
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
    
    name2 = dt.now().isoformat("_", "seconds") + ".mp3"
    bash(f'ffmpeg -i {"2" + out} -b:a 128k {name2} -y')
    new_name = file.split(".")[-2] + ".mp3"
    os.rename(name2, new_name)
    return new_name
 
