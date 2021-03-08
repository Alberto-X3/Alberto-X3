import discord
import Utils

from datetime import timedelta


HELP = Utils.Help(vanish=True, order_1793=True)
EVENTS = [Utils.EVENT.on_message]


async def __main__(client: discord.Client, _event: int, message: discord.Message):
    try:
        if message.author.bot:
            return

        async for message_ in message.channel.history(limit=20, before=message.created_at):
            message_: discord.Message

            if message_.author == message.author and not message_.author == client.user:
                if message_.content == message.content:
                    if message.created_at - message_.created_at > timedelta(minutes=30):
                        break
                    await message.delete()
                    await message.channel.send(f"**__Anti-spam__**\n:x: Please don't spam {message.author.mention}!", delete_after=5)
                break

    except Exception as e:
        import datetime
        super_log: discord.TextChannel = client.get_channel(Utils.DATA.IDs.Channels.Super_Log)

        embed: discord.Embed = discord.Embed(title=__name__,
                                             description=f"{e.__class__.__name__}: {e.__str__()}\n",
                                             color=discord.Color.magenta())

        embed.add_field(name="datetime.datetime",
                        value=datetime.datetime.utcnow().isoformat().replace("T", ""))

        await super_log.send(embed=embed)
