import discord
import Utils


HELP = Utils.Help(f"shows you your permissions", f"""
> *{Utils.Prefix}perms*
shows you your perms

> *{Utils.Prefix}perms [USER-ID|USER-MENTION]*
shows you perms from other

> *{Utils.Prefix}perms [USER-ID|USER-MENTION] [add|+] [PERMISSION]*
adds permissions for a user

> *{Utils.Prefix}perms [USER-ID|USER-MENTION] [remove|-] [PERMISSION]*
removes permissions from a user

""")
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["p"]


async def __main__(client: discord.Client, _event: int, message: discord.Message):

    user_perms = Utils.perms(str(message.author.id))

    # not 'seeOwn'
    if len(message.content.split()) > 1:

        if message.content.split()[1].replace("<", "").replace("@", "").replace("!", "").replace(">", "").isnumeric() and len(message.content.split()) == 2:

            # 'seeOther'
            if len(message.content.split()) == 2:

                if user_perms.User.Perms.seeOther:
                    await perms(message, message.content.split()[1].replace("<", "").replace("@", "").replace("!", "").replace(">", ""), Utils.perms(message.content.split()[1].replace("<", "").replace("@", "").replace("!", "").replace(">", "")))

                else:
                    await message.channel.send(":x: requires User.Perms.seeOther")

        # 'set'
        elif len(message.content.split()) == 4:
            if message.content.split()[1].replace("<", "").replace("@", "").replace("!", "").replace(">", "").isnumeric():

                if message.content.split()[2] == "add" or message.content.split()[2] == "+":
                    await set_(message, user_perms, True)

                elif message.content.split()[2] == "remove" or message.content.split()[2] == "-":
                    await set_(message, user_perms, False)

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


def replace(root: Utils.Union[Utils.AttrDict, bool], keys: list, value: Utils.Any):
    if not keys:
        return value
    else:
        root[keys[0]] = replace(root[keys[0]], keys[1:], value)
        return root


def replaces(root: Utils.Union[Utils.AttrDict, bool], value: Utils.Optional[bool]):
    for key in root:
        if isinstance(root[key], bool):
            root[key] = value
        else:
            root[key] = replaces(root[key], value)
    return root


async def set_(message: discord.Message, user_perms: Utils.AttrDict, new: bool):
    if user_perms.User.Perms.set or message.author.id == Utils.DATA.Author_id:

        try:
            perm = eval(f"user_perms.{message.content.split()[-1]}")
        except KeyError:
            await message.channel.send(":x: This permission doesn't exist! :x:")
        else:
            id_ = message.content.split()[1].replace("<", "").replace("@", "").replace("!", "").replace(">", "")
            if id_ == str(message.author.id) and not message.author.id == Utils.DATA.Author_id:
                await message.channel.send("**__:x: Please don't modify yourself! :x:__**\nhere is a 🃏 for you \\:)")
                return

            root = Utils.perms(id_)
            keys = message.content.split()[-1].split('.')
            if isinstance(perm, bool):
                if perm:
                    new_perms = replace(root, keys, new)

                else:
                    await message.channel.send(":x: You don't have this permission! :x:")
                    return
            else:
                if new is False:
                    if user_perms.User.Perms.removeMultiple:
                        new_perms = replace(root, keys, replaces(eval(f"root.{message.content.split()[-1]}"), new))
                    else:
                        await message.channel.send(":x: You don't have permissions to remove multiple permissions at once! :x:")
                        return
                else:
                    if message.author.id == Utils.DATA.Author_id:
                        new_perms = replace(root, keys, replaces(eval(f"root.{message.content.split()[-1]}"), new))
                    else:
                        await message.channel.send(":x: You don't have permissions to add multiple permissions at once! :x:")
                        return

            from json import load, dump
            permissions = Utils.AttrDict(load(open("perms.json")))
            permissions[id_] = new_perms
            dump(permissions, open("perms.json", "w"), indent=2)

            await message.channel.send(f"**Successfully {'added permissions to' if new is True else 'removed permissions from'} <@{id_}>**")

    else:
        await message.channel.send(":x: requires User.Perms.set")
