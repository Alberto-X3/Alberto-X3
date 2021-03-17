import discord
import Utils
import datetime


HELP = Utils.Help("shows the ping")
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["🏓"]


async def __main__(client: discord.Client, _event: int, message: discord.Message):
    try:
        api: float = round(client.latency, 2)
        msg: float = round((datetime.datetime.utcnow() - message.created_at).total_seconds(), 2)

        await message.channel.send(f"Pong 🏓\n> API latency: {api} seconds\n> Message latency: {msg} seconds")

    except Exception as e:
        await Utils.send_exception(client=client, exception=e, source_name=__name__)
