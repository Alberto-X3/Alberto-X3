import discord
import Utils

from json import load


EVENTS = [Utils.EVENT.on_raw_reaction_add]


async def __main__(client: discord.Client, _event: int, reaction: discord.RawReactionActionEvent):

    DATA = Utils.AttrDict(load(open("Configs.json")))

    logger = Utils.Logger(channel=await client.fetch_channel(DATA.IDs.Channels.Logs))

    channel_id = DATA.IDs.Channels.Rules
    message_id = DATA.IDs.Messages.Rules
    role_id = DATA.IDs.Roles.Rules
    guild: discord.Guild = client.get_guild(reaction.guild_id)
    role = discord.utils.get(guild.roles, id=role_id)

    if reaction.channel_id == channel_id:
        if reaction.message_id == message_id:
            if reaction.emoji.name == "✅":
                if role not in reaction.member.roles:
                    await reaction.member.add_roles(role, reason="Rules accepted...")
                    await logger.rules(user=reaction.member.user)
                channel: discord.TextChannel = client.get_channel(id=reaction.channel_id)
                message: discord.Message = await channel.fetch_message(reaction.message_id)

                await message.remove_reaction(emoji=reaction.emoji, member=reaction.member)
