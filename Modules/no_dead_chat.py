"""
deletes message with "https://tenor.com/view/pacman-gif-21447981" only
content and sends "https://tenor.com/view/server-chat-is-dead-stayin-alive-ive-been-kick-aroud-active-members-gif-17860742"
to the chat
"""
from discord import Message, Client
from Utils import Help, EVENT, send_exception


HELP = Help(vanish=True, order_1793=True)
EVENTS = [EVENT.on_message]

BAD = "https://tenor.com/view/pacman-gif-21447981"
GOOD = "https://tenor.com/view/server-chat-is-dead-stayin-alive-ive-been-kick-aroud-active-members-gif-17860742"


async def __main__(client: Client, _event: int, message: Message):
    try:
        if message.author.id == client.user.id:
            return

        if message.content == BAD:
            await message.reply(GOOD)
            await message.delete()

    except Exception as e:
        await send_exception(client=client, exception=e, source_name=__name__)
