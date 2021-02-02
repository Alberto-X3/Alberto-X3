import discord
import Utils

from json import load


EVENTS = [Utils.EVENT.on_ready]


async def __main__(client: discord.Client, _event: int):

    DATA = Utils.AttrDict(load(open("Configs.json")))

    logger = Utils.Logger(channel=await client.fetch_channel(DATA.IDs.Channels.Logs))

    guild:   discord.guild = client.get_guild(id=632526390113337346)
    role:    discord.Role = discord.utils.get(guild.roles, id=DATA.IDs.Roles.Rules)
    channel: discord.TextChannel = await client.fetch_channel(DATA.IDs.Channels.Rules)
    message: discord.Message = await channel.fetch_message(DATA.IDs.Messages.Rules)

    for reaction in message.reactions:
        async for member in reaction.users():

            if member == client.user:
                continue

            if role not in member.roles:
                await member.add_roles(role, reason="Rules accepted...")
                await logger.rules(user=member.user)

            await message.remove_reaction(emoji=reaction.emoji, member=member)

