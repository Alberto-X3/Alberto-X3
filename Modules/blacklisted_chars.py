"""
deletes all messages with blacklisted content
"""
from discord import Message, Client
from Utils import Help, EVENT, send_exception


HELP = Help(vanish=True, order_1793=True)
EVENTS = [EVENT.on_message]

BLACKLISTED = (
    "\u200b",
    "\u200c",
    "\u200d",
)


async def __main__(client: Client, _event: int, message: Message):
    try:
        if message.author.id == client.user.id:
            return

        c = message.content or ""
        for b in BLACKLISTED:
            if b in c:
                await message.delete()
                break

    except Exception as e:
        await send_exception(client=client, exception=e, source_name=__name__)
