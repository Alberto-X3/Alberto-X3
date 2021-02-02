import discord
import Utils
import datetime

from json import load


EVENTS = [Utils.EVENT.on_member_join]


async def __main__(client: discord.Client, _event: int, member: discord.Member):

    DATA = Utils.AttrDict(load(open("Configs.json")))
    user = await client.fetch_user(member.user.id)
    channel = await client.fetch_channel(DATA.IDs.Channels.Welcome)

    embed = discord.Embed(title=f"Member {user} joined us!", description="Here some Information:", color=DATA.colors.green)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Account creation:", value=f"{user.created_at}\n{(datetime.datetime.now() - user.created_at).days} days ago", inline=False)
    embed.add_field(name="Name:", value=user.name, inline=False).add_field(name="ID:", value=user.id, inline=False)

    await channel.send(embed=embed)
    await Utils.Logger(channel=await client.fetch_channel(DATA.IDs.Channels.Logs)).join(user=user)
