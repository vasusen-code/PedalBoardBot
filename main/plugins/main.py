import time
from telethon import events, Button
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from ethon.telefunc import fast_download, fast_upload

from .. import Drone, ACCESS_CHANNEL
from .pedalboard import slow_n_reverb

process = []

THUMB="./main/plugins/rombo-t1gKqulJW2c-unsplash.jpg"

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
    try:
        x = await Drone(GetParticipantRequest(channel="save_restricted_content_1", participant=int(id)))
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
    
    # await event.forward_to(int(ACCESS_CHANNEL))


    if event.audio or 'audio' in event.file.mime_type or \
    event.media and (str(event.file.name)).split(".")[-1] == "ogg":
        
        x = await force_sub(event.sender_id)
        if x != False:
            return await event.reply("⚠️ You've to join my parent channels to use this bot.", buttons=[[Button.url("Join DroneBOTs", url="t.me/DroneBots")], [Button.url("Join SRC", url="t.me/Save_restricted_content_1")]])
            
        if event.sender_id in process:
            return event.reply("Wait until your previous process finish!🕰")
        
        try:
            process.append(int(event.sender_id))
            if hasattr(event.media, "document"):
                file = event.media.document
            else:
                file = event.media
            reply = await event.reply("**📟PROCESSING**")
            edit = await Drone.send_message(ACCESS_CHANNEL, "...")
            await reply.edit("**DOWNLOADING⌨**")
            name = event.file.name
            if name is None:
                name = f'{int(time.time()) + event.sender_id}.mp3'
            await fast_download(name, file, event.client, edit, time.time(), "**DOWNLOADING⌨**")
            await reply.edit("**🎛PRODUCING**")
            out = slow_n_reverb(name)
            await reply.edit('**UPLOADING🚀**')
            uploader = await fast_upload(out, out, time.time(), Drone, edit, '**UPLOADING🚀**')
            await Drone.send_file(event.chat_id, uploader, caption=f"**Produced by** : @PedalBoardBot", thumb=THUMB)
            process.pop(process.index(int(event.sender_id)))
            await reply.delete()
            await edit.delete()
        except Exception as e:
            process.pop(process.index(int(event.sender_id)))
            print(e)
            await reply.edit(f"⚠️ Sorry! but Something went wrong, contact @TeamDrone.\n\n**ERROR:** {str(e)}")
            
            
                
