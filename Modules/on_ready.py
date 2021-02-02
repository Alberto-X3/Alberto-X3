import discord
import Utils

from json import load


EVENTS = [Utils.EVENT.on_ready]


async def __main__(client: discord.Client, _event: int):

    DATA = Utils.AttrDict(load(open("Configs.json")))
    Prefix = DATA.CONSTANTS.Prefix

    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Activity(name=f"{Prefix}help", type=discord.ActivityType.listening), status=discord.Status.online)
