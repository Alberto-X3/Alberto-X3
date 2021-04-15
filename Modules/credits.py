import discord
import Utils

HELP = Utils.Help("displays the credits", "here are the credits with the code...")
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["c", "code"]


async def __main__(client: discord.Client, _event: int, message: discord.Message):
    try:
        await message.channel.send(embed=discord.Embed(description=f"""
    ~~Modular Code: [here](https://github.com/AlbertUnruh/ModularDiscordPyBot)~~
    My Code: [here](https://github.com/AlbertUnruh/Alberto-X3)

    source code by <@546320163276849162>
    profile pictures by <@665288034274639873>
    """))

    except Exception as e:
        await Utils.send_exception(client=client, exception=e, source_name=__name__)
