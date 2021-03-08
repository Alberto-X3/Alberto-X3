import discord
import Utils

from json import load


HELP = Utils.Help("unbans a user with the given iD", f"_{Utils.Prefix}unban iD (reason)_\nrequires Admin.unban")
EVENTS = [Utils.EVENT.on_message]
ALIASES = []


async def __main__(client: discord.Client, _event: int, message: discord.Message):
    try:
        user_perms = Utils.perms(str(message.author.id))
        DATA = Utils.AttrDict(load(open("Configs.json")))

        if user_perms.Admin.ban:
            if len(message.content.split()) >= 2:
                if message.content.split()[1].isnumeric():
                    if len(message.content.split()) > 2:
                        reason = message.content.split(maxsplit=2)[2]
                    else:
                        reason = "No reason..."

                    logger = Utils.Logger(channel=await client.fetch_channel(DATA.IDs.Channels.Logs))
                    channel: discord.TextChannel = message.channel
                    guild:         discord.Guild = message.guild
                    user:           discord.User = await client.fetch_user(int(message.content.split()[1]))
                    handler:        discord.User = message.author

                    try:
                        await guild.unban(user=user, reason=reason)
                        await logger.unban(user=handler, target=user, reason=reason)
                        # await user.send(f"You where unbanned from the {guild} Server.\n_{reason}_")  # they have to be on a same guild
                        await message.delete()
                    except ValueError:
                        await channel.send(":x: ERROR :x:")
                    except discord.Forbidden:
                        pass

                else:
                    await message.channel.send(f":x: Please enter the User-iD")
            else:
                await message.channel.send(f":x: Please enter the User-iD")

        else:
            await message.channel.send(":x: requires Admin.unban")

    except Exception as e:
        import datetime
        super_log: discord.TextChannel = client.get_channel(Utils.DATA.IDs.Channels.Super_Log)

        embed: discord.Embed = discord.Embed(title=__name__,
                                             description=f"{e.__class__.__name__}: {e.__str__()}\n",
                                             color=discord.Color.magenta())
        embed.add_field(name="datetime.datetime",
                        value=datetime.datetime.utcnow().isoformat())

        await super_log.send(embed=embed)
