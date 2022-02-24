from telethon import events

from .. import Drone

welcome = """👋🎧Heya, 

I'm PedalBoard, send me any audio."""

@Drone.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    await event.client.send_message(event.chat_id, welcome, reply_to=event.id)
    
