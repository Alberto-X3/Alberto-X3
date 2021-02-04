import discord
import Utils


HELP = Utils.Help(vanish=True, order_1793=True)
EVENTS = [Utils.EVENT.on_message]


async def __main__(client: discord.Client, _event: int, message: discord.Message):
    if message.content == client.user.mention:
        await message.channel.send(f"My Prefix is `{Utils.Prefix}`")
