import discord
import Utils


HELP = Utils.Help("~~kills the Bot...~~ really dangerous", "is very dangerous... so be careful with it\nrequires Admin.Bot.kill")
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["most-dangerous-cmd"]


async def __main__(client: discord.Client, _event: int, message: discord.Message):
    try:
        user_perms = Utils.perms(str(message.author.id))

        if user_perms.Admin.Bot.kill:
            coder = await client.fetch_user(Utils.DATA.Author_id)
            await coder.send(f"**__starting kill by {message.author}__**")
            await client.change_presence(status=discord.Status.offline)
            await client.close()

            input("Press <ENTER>...")

        else:
            await message.channel.send(":x: requires Admin.Bot.kill")

    except Exception as e:
        import datetime
        super_log: discord.TextChannel = client.get_channel(Utils.DATA.IDs.Channels.Super_Log)

        embed: discord.Embed = discord.Embed(title=__name__,
                                             description=f"{e.__class__.__name__}: {e.__str__()}\n",
                                             color=discord.Color.magenta())
        embed.add_field(name="datetime.datetime",
                        value=datetime.datetime.utcnow().isoformat().replace("T", ""))

        await super_log.send(embed=embed)
