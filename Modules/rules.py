import discord
import Utils


EVENTS = [Utils.EVENT.on_raw_reaction_add, Utils.EVENT.on_ready]


async def __main__(client: discord.Client, _event: int, reaction: discord.RawReactionActionEvent = None):
    try:
        if _event == Utils.EVENT.on_raw_reaction_add:
            await accept(client, reaction)

        if _event == Utils.EVENT.on_ready:
            await accepted(client)

    except Exception as e:
        await Utils.send_exception(client=client, exception=e, source_name=__name__)


async def accept(client: discord.Client, reaction: discord.RawReactionActionEvent):

    if reaction.member == client.user:
        return

    logger = Utils.Logger(channel=await client.fetch_channel(Utils.DATA.IDs.Channels.Logs))

    channel_id = Utils.DATA.IDs.Channels.Rules
    message_id = Utils.DATA.IDs.Messages.Rules
    role_id = Utils.DATA.IDs.Roles.Rules
    guild: discord.Guild = client.get_guild(reaction.guild_id)
    role = discord.utils.get(guild.roles, id=role_id)
    news = discord.utils.get(guild.roles, id=831831226146750484)

    if reaction.channel_id == channel_id:
        if reaction.message_id == message_id:
            if reaction.emoji.name == "✅":
                if role not in reaction.member.roles:
                    await reaction.member.add_roles(role, reason="Rules accepted...")
                    await logger.rules(user=reaction.member)
            channel: discord.TextChannel = client.get_channel(id=reaction.channel_id)
            message: discord.Message = await channel.fetch_message(reaction.message_id)

            if reaction.emoji.name == "📯":
                await reaction.member.add_roles(news)

            if reaction.emoji.name == "❌":
                await reaction.member.remove_roles(news)

            await message.add_reaction("✅")
            await message.add_reaction("📯")
            await message.add_reaction("❌")
            await message.remove_reaction(emoji=reaction.emoji, member=reaction.member)


async def accepted(client: discord.Client):

    logger = Utils.Logger(channel=await client.fetch_channel(Utils.DATA.IDs.Channels.Logs))

    guild:   discord.guild = client.get_guild(id=632526390113337346)
    role:    discord.Role = discord.utils.get(guild.roles, id=Utils.DATA.IDs.Roles.Rules)
    news:    discord.Role = discord.utils.get(guild.roles, id=831831226146750484)
    channel: discord.TextChannel = await client.fetch_channel(Utils.DATA.IDs.Channels.Rules)
    message: discord.Message = await channel.fetch_message(Utils.DATA.IDs.Messages.Rules)

    for reaction in message.reactions:
        async for member in reaction.users():

            if member == client.user:
                continue

            if role not in member.roles and reaction.emoji.name == "✅":
                await member.add_roles(role, reason="Rules accepted...")
                await logger.rules(user=member)

            if role not in member.roles and reaction.emoji.name == "📯":
                await member.add_roles(news)

            if role not in member.roles and reaction.emoji.name == "❌":
                await member.remove_roles(news)

            await message.remove_reaction(emoji=reaction.emoji, member=member)
