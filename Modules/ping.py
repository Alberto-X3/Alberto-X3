import discord
import Utils


HELP = Utils.Help("shows the ping")
EVENTS = [Utils.EVENT.on_message]
ALIASES = []


async def __main__(client: discord.Client, _event: int, message: discord.Message):
    await message.channel.send(round(client.latency, 2))
