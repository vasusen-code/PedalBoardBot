import time
from telethon import events
from ethon import fast_download, fast_upload

from .. import Drone
from .pedalboard import slow_n_reverb

process = []

@Drone.on(events.NewMessage(incoming=True,func=lambda e: e.is_private))
async def new(event):
    
    if event.audio:
        
        if event.sender_id in process:
            return event.reply("Wait until your previous process finish!🕰")
        
        try:
            process.append(int(event.sender_id))
            reply = await event.reply("📟Processing...")
            await fast_download(event.file.name, event.media, event.client, reply, time.time(), "**DOWNLOADING⌨**")
            out = slow_n_reverb(event.file.name)
            uploader = await fast_upload(out, out, time.time(), Drone, reply, '**UPLOADING🚀**')
            await Drone.send_file(event.chat_id, uploader, caption=f"**Produced by** : @PedalBoardBot", thumb=THUMB)
            process.pop(process.index(int(event.sender_id)))
        except Exception as e:
            process.pop(process.index(int(event.sender_id)))
            print(e)
            await reply.edit("Sorry! but Something went wrong, contact @TeamDrone.")
            
            
                
