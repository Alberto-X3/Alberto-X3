import discord
import Utils

from json import load

DATA = Utils.AttrDict(load(open("Configs.json")))
Prefix = DATA.CONSTANTS.Prefix

HELP = Utils.Help(f"shows you your permissions", f"""
> *{Prefix}perms*
shows you your perms

> *{Prefix}perms [USER-ID|USER-MENTION]*
shows you perms from other

> *{Prefix}perms [add|+] [USER-ID|USER-MENTION] [PERMISSION]*
adds permissions for a user

> *{Prefix}perms [remove|-] [USER-ID|USER-MENTION] [PERMISSION]*
removes permissions from a user
""")
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["p"]


async def __main__(client: discord.Client, _event: int, message: discord.Message):

    user_perms = Utils.perms(str(message.author.id))

    # not 'seeOwn'
    if len(message.content.split()) > 1:

        if message.content.split()[1].replace("<", "").replace("@", "").replace("!", "").replace(">", "").isnumeric():

            # 'seeOther'
            if len(message.content.split()) == 2:

                if user_perms.User.Perms.seeOther:
                    await perms(message, message.content.split()[1].replace("<", "").replace("@", "").replace("!", "").replace(">", ""), Utils.perms(message.content.split()[1].replace("<", "").replace("@", "").replace("!", "").replace(">", "")))

                else:
                    await message.channel.send(":x: requires User.Perms.seeOther")

        # 'set'
        elif len(message.content.split()) == 4:
            if message.content.split()[2].replace("<", "").replace("@", "").replace("!", "").replace(">", "").isnumeric():

                if message.content.split()[1] == "add" or message.content.split()[1] == "+":
                    await add(message, user_perms)

                elif message.content.split()[1] == "remove" or message.content.split()[1] == "-":
                    await remove(message, user_perms)

            else:
                await message.channel.send(":x: Please enter a ID or a MENTION")

        else:
            await message.channel.send(":x: Invalid Syntax")

    # 'seeOwn'
    else:
        if user_perms.User.Perms.seeOwn:
            await perms(message, str(message.author.id), user_perms)

        else:
            await message.channel.send(":x: requires User.Perms.seeOwn")


def finder(data: Utils.AttrDict, path="") -> list:
    found = []
    for key in data.__dict__:
        if isinstance(data[key], Utils.AttrDict):
            found += finder(data[key], f"{path}{'.' if path else ''}{key}")
        else:
            found += [f"{path}{'.' if path else ''}{key}"] if data[key] else []
    return found


async def perms(message: discord.Message, _id: str, user_perms: Utils.AttrDict):

    log = "\n".join(finder(user_perms))
    await message.channel.send(f"**__perms from <@{_id}>:__**\n{log}")


async def add(message: discord.Message, user_perms: Utils.AttrDict):
    if user_perms.User.Perms.set:
        await message.channel.send(":x: Not implemented yet :x:")

    else:
        await message.channel.send(":x: requires User.Perms.set")


async def remove(message: discord.Message, use_perms: Utils.AttrDict):
    if use_perms.User.Perms.set:
        await message.channel.send(":x: Not implemented yet :x:")

    else:
        await message.channel.send(":x: requires User.Perms.set")
