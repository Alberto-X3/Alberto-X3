import discord
import Utils
from NewClass import AttrDict
from json import load

HELP = Utils.Help("displays the credits", "here are the credits with the code...")
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["c"]


async def __main__(client: discord.Client, _event: int, message: discord.Message):

    configs = AttrDict(load(open("Configs.json")))
    author = configs.Author

    await message.channel.send(embed=discord.Embed(description=f"""
The Author is {author}
Modular Code: [here](https://github.com/AlbertUnruh/ModularDiscordPyBot)
My Code: [here](https://github.com/AlbertUnruh/Alberto-X3)
"""))
