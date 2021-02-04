import discord
import Utils

from json import load


Prefix = Utils.AttrDict(load(open("Configs.json"))).CONSTANTS.Prefix

HELP = Utils.Help(f"requires Admin.Bot.kick", f"_{Prefix}kick iD (reason)_")
EVENTS = [Utils.EVENT.on_message]


async def __main__(client: discord.Client, _event: int, message: discord.Message):

    user_perms = Utils.perms(str(message.author.id))
    DATA = Utils.AttrDict(load(open("Configs.json")))

    if user_perms.Admin.kick:
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
                    await user.send(f"You where kicked from the {guild} Server.\n_{reason}_")
                    await guild.kick(user=user, reason=reason)
                    await logger.kick(user=handler, target=user, reason=reason)
                    await message.delete()
                except ValueError:
                    await channel.send(":x: ERROR :x:")
                except discord.Forbidden:
                    pass

            else:
                await message.channel.send(":x: Please enter the User-iD")
        else:
            await message.channel.send(":x: Please enter the User-iD")

    else:
        await message.channel.send(":x: requires Admin.kick")
