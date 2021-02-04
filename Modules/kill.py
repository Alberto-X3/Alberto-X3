import discord
import Utils

from json import load


HELP = Utils.Help("requires Admin.Bot.kill\n~~kills the Bot...~~ really dangerous")
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["most-dangerous-cmd"]


async def __main__(client: discord.Client, _event: int, message: discord.Message):

    user_perms = Utils.perms(str(message.author.id))

    if user_perms.Admin.Bot.kill:
        coder = await client.fetch_user(Utils.AttrDict(load(open("./Configs.json"))).Author_id)
        await coder.send(f"**__starting kill by {message.author}__**")
        await client.change_presence(status=discord.Status.offline)
        await client.close()

        input("Press <ENTER>...")

    else:
        await message.channel.send(":x: requires Admin.Bot.kill")
