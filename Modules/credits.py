import discord
import Utils

HELP = Utils.Help("displays the credits", "here are the credits with the code...")
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["c"]


async def __main__(client: discord.Client, _event: int, message: discord.Message):
    try:
        author = Utils.DATA.Author

        await message.channel.send(embed=discord.Embed(description=f"""
    The Author is {author}
    Modular Code: [here](https://github.com/AlbertUnruh/ModularDiscordPyBot)
    My Code: [here](https://github.com/AlbertUnruh/Alberto-X3)
    """))

    except Exception as e:
        from discord.utils import snowflake_time

        super_log: discord.TextChannel = client.get_channel(Utils.DATA.IDs.Channels.Super_Log)
        embed: discord.Embed = discord.Embed(title=__name__,
                                             description=f"{e.__class__.__name__}: {e.__str__()}\n",
                                             color=discord.Color.magenta())

        message: discord.Message = await super_log.send(embed=embed)

        embed.add_field(name="datetime.datetime",
                        value=snowflake_time(message.id).__str__())
        await message.edit(embed=embed)
        await message.pin()
        await super_log.send(f"<@&{820974562770550816}>", delete_after=0)
