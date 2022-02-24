import wave, soundfile as sf, pedalboard as p, datetime, ethon

def slow_n_reverb(file):
    out = datetime.datetime.now().isoformat("_", "seconds") + ".wav"
    ethon.pyfunc.bash(f'ffmpeg -i {file} {out})
    
    # Slow down audio
    CHANNELS = 1 
    swidth = 4
    Change_RATE = 0.75
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
    board = p.Pedalboard([p.Reverb(room_size=0.04)])
    effected = board(audio, sample_rate)
    sf.write("2" + out, effected, sample_rate)
    return "2" + out
 
