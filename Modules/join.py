import discord
import Utils
import datetime


EVENTS = [Utils.EVENT.on_member_join]


async def __main__(client: discord.Client, _event: int, member: discord.Member):
    try:
        user = await client.fetch_user(member.id)
        channel = await client.fetch_channel(Utils.DATA.IDs.Channels.Welcome)

        embed = discord.Embed(title=f"Member {user.__str__()} joined us!", description="Here some Information:", color=Utils.DATA.colors.green)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Account creation:", value=f"{user.created_at}\n{(datetime.datetime.now() - user.created_at).days} days ago", inline=False)
        embed.add_field(name="Name:", value=user.name, inline=False).add_field(name="ID:", value=user.id, inline=False)

        await channel.send(embed=embed)
        await Utils.Logger(channel=await client.fetch_channel(Utils.DATA.IDs.Channels.Logs)).join(user=user)

    except Exception as e:
        super_log: discord.TextChannel = client.get_channel(Utils.DATA.IDs.Channels.Super_Log)

        embed: discord.Embed = discord.Embed(title=__name__,
                                             description=f"{e.__class__.__name__}: {e.__str__()}\n",
                                             color=discord.Color.magenta())
        await super_log.send(embed=embed)
