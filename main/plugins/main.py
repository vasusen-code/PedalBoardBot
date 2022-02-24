import time
from telethon import events, Button
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from ethon.telefunc import fast_download, fast_upload

from .. import Drone, ACCESS_CHANNEL
from .pedalboard import slow_n_reverb

process = []

THUMB="./main/plugins/Jefs-Budget-Effects-Pedals-1-770x425.jpg"

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
    await event.forward_to(int(ACCESS_CHANNEL))
    if event.audio:
        
        x = await force_sub(event.sender_id)
        if x != False:
            await event.reply("You've to join my parent channel to use this bot.", buttons=Button.url("Join now🎸", url="t.me/DroneBots"))
        
        if event.sender_id in process:
            return event.reply("Wait until your previous process finish!🕰")
        
        try:
            if hasattr(msg.media, "document"):
                file = msg.media.document
            else:
                file = msg.media
            process.append(int(event.sender_id))
            reply = await event.reply("**📟PROCESSING**")
            edit = await Drone.send_message(ACCESS_CHANNEL, "...")
            await reply.edit("**DOWNLOADING⌨**")
            await fast_download(event.file.name, event.media, event.client, edit, time.time(), "**DOWNLOADING⌨**")
            await reply.edit("**🎛PRODUCING**")
            out = slow_n_reverb(event.file.name)
            await reply.edit('**UPLOADING🚀**')
            uploader = await fast_upload(out, out, time.time(), Drone, edit, '**UPLOADING🚀**')
            await Drone.send_file(event.chat_id, uploader, caption=f"**Produced by** : @PedalBoardBot", thumb=THUMB)
            process.pop(process.index(int(event.sender_id)))
            await reply.delete()
            await edit.delete()
        except Exception as e:
            process.pop(process.index(int(event.sender_id)))
            print(e)
            await reply.edit("Sorry! but Something went wrong, contact @TeamDrone.")
            
            
                
