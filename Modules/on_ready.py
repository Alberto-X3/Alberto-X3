import discord
import Utils


EVENTS = [Utils.EVENT.on_ready]


async def __main__(client: discord.Client, _event: int):

    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Activity(name=f"{Utils.Prefix}help", type=discord.ActivityType.listening), status=discord.Status.online)
