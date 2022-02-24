from telethon import events

@Drone.on(events.NewMessage(incoming=True,func=lambda e: e.is_private))
async def new(event):
    if event.audio:
        await event.reply("Processing
