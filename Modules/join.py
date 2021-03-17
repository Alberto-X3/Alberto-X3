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
        await Utils.send_exception(client=client, exception=e, source_name=__name__)
