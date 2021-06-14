import discord
import Utils
import datetime


EVENTS = [Utils.EVENT.on_member_join, Utils.EVENT.on_member_remove]


async def __main__(client: discord.Client, _event: int, member: discord.Member):
    try:
        channel = await client.fetch_channel(Utils.DATA.IDs.Channels.Welcome)

        if _event == Utils.EVENT.on_member_join:
            embed = discord.Embed(title=f"Member {member} joined us!",
                                  description=f"Here some Information about "
                                              f"{member.mention}:",
                                  color=Utils.DATA.colors.green)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Account creation:",
                            value=f"{member.created_at}\n"
                                  f"{(datetime.datetime.now() - member.created_at).days} days ago",
                            inline=False)
            embed.add_field(name="Name:",
                            value=member.name,
                            inline=False)
            embed.add_field(name="ID:",
                            value=member.id,
                            inline=False)
            await Utils.Logger(channel=await client.fetch_channel(Utils.DATA.IDs.Channels.Logs)).join(member=member)

        else:
            embed = discord.Embed(title=f"(ex-) Member {member} left us!",
                                  description=f"Here some Information about "
                                              f"{member.mention}:",
                                  color=Utils.DATA.colors.red)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Account creation:",
                            value=f"{member.created_at}\n"
                                  f"{(datetime.datetime.now() - member.created_at).days} days ago",
                            inline=False)
            embed.add_field(name="Server joined:",
                            value=f"{member.joined_at}\n"
                                  f"{(datetime.datetime.now() - member.joined_at).days} days ago",
                            inline=False)
            embed.add_field(name="Name:",
                            value=member.name,
                            inline=False)
            embed.add_field(name="ID:",
                            value=member.id,
                            inline=False)
            await Utils.Logger(channel=await client.fetch_channel(Utils.DATA.IDs.Channels.Logs)).left(member=member)

        await channel.send(embed=embed)

    except Exception as e:
        await Utils.send_exception(client=client, exception=e, source_name=__name__)
