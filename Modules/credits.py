import discord
import Utils

HELP = Utils.Help("displays the credits", "here are the credits with the code...")
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["c"]


async def __main__(client: discord.Client, _event: int, message: discord.Message):

    author = Utils.DATA.Author

    await message.channel.send(embed=discord.Embed(description=f"""
The Author is {author}
Modular Code: [here](https://github.com/AlbertUnruh/ModularDiscordPyBot)
My Code: [here](https://github.com/AlbertUnruh/Alberto-X3)
"""))
