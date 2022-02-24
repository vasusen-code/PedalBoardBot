import time
from telethon import events
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from ethon import fast_download, fast_upload

from .. import Drone
from .pedalboard import slow_n_reverb

process = []

THUMB="./main/plugins/"

async def force_sub(id):
    ok = False
    try:
        x = await Drone(GetParticipantRequest(channel="DroneBots", participant=int(id)))
        left = x.stringify()
        if 'left' in left:
            ok = True
        else:
            ok = False
    except UserNotParticipantError:
        ok = True 
    return ok

@Drone.on(events.NewMessage(incoming=True,func=lambda e: e.is_private))
async def new(event):
    
    if event.audio:
        
        x = await force_sub(event.sender_id)
        if x != False:
            await event.reply("You've to join my parent channel to use this bot.", buttons=Button.url("Join now🎸", url="t.me/DroneBots"))
        
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
            
            
                
