import discord
import Utils


HELP = Utils.Help(_help="Is a module for debugging the bot", vanish=True)
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["db", "debug", "bug", "bugs", "exception", "exceptions", "error", "errors"]


async def __main__(client: discord.Client, _event: int, message: discord.Message):
    try:
        if hasattr(message.author, "roles"):
            if any(role.id == 820974562770550816 for role in message.author.roles):
                Utils.DATA.debug = not Utils.DATA.debug
                await message.channel.send(f"Toggled `debug` to `{Utils.DATA.debug}`")

        else:
            await message.channel.send("Please use me on a server!")

    except Exception as e:
        await Utils.send_exception(client=client, exception=e, source_name=__name__)
