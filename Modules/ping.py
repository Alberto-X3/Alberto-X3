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
        super_log: discord.TextChannel = client.get_channel(Utils.DATA.IDs.Channels.Super_Log)

        embed: discord.Embed = discord.Embed(title=__name__,
                                             description=f"{e.__class__.__name__}: {e.__str__()}\n",
                                             color=discord.Color.magenta())
        embed.add_field(name="datetime.datetime",
                        value=datetime.datetime.utcnow().isoformat().replace("T", " "))

        await super_log.send(embed=embed)
