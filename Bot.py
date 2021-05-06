from typing import *
from asyncio import create_task

import datetime
import discord
import Modules
import Utils

# to be sure, that there is a DB
import levels_config_sqlite
del levels_config_sqlite


intents = discord.Intents.all()
client = discord.Client(intents=intents)
TOKEN = Utils.DATA.CONSTANTS.Token
Prefix = Utils.Prefix


exceptions = True
# this boolean tells you, if your code will actually throw a error (what isn't so mad...) or
# that you get the errors in your cmd (this is my favorite, because you know exactly what for
# a error it exactly is (and where you can find it in your code))
#
# `True` normal errors in the cmd (default)
# `False` just a feedback, in what for a event a error was raised


'''
You can see all the events in the following URL:
https://discordpy.readthedocs.io/en/latest/api.html#event-reference
'''


@client.event
async def on_connect():

    for module in Modules.MODULES:
        if Utils.EVENT.on_connect in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_connect))


@client.event
async def on_shard_connect(shard_id: int):

    for module in Modules.MODULES:
        if Utils.EVENT.on_shard_connect in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_shard_connect, shard_id))


@client.event
async def on_disconnect():

    for module in Modules.MODULES:
        if Utils.EVENT.on_disconnect in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_disconnect))


@client.event
async def on_shard_disconnect(shard_id: int):

    for module in Modules.MODULES:
        if Utils.EVENT.on_shard_disconnect in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_shard_disconnect, shard_id))


@client.event
async def on_ready():

    for module in Modules.MODULES:
        if Utils.EVENT.on_ready in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_ready))


@client.event
async def on_shard_ready(shard_id: int):

    for module in Modules.MODULES:
        if Utils.EVENT.on_shard_ready in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_shard_ready, shard_id))


@client.event
async def on_resumed():

    for module in Modules.MODULES:
        if Utils.EVENT.on_resumed in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_resumed))


@client.event
async def on_shard_resumed(shard_id: int):

    for module in Modules.MODULES:
        if Utils.EVENT.on_shard_resumed in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_shard_resumed, shard_id))


if not exceptions:
    @client.event
    async def on_error(event: str, *args, **kwargs):
        print("ERROR BY DC!!!")
        print(f"{event=}")
        print(f"{args=}")
        print(f"{kwargs=}")

        for module in Modules.MODULES:
            if Utils.EVENT.on_error in Modules.libs[module].EVENTS:

                create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_error, event, *args, **kwargs))


@client.event
async def on_socket_raw_receive(msg: Union[bytes, str]):

    for module in Modules.MODULES:
        if Utils.EVENT.on_socket_raw_receive in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_socket_raw_receive, msg))


@client.event
async def on_socket_raw_send(payload: Union[bytes, str]):

    for module in Modules.MODULES:
        if Utils.EVENT.on_socket_raw_send in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_socket_raw_send, payload))


@client.event
async def on_typing(channel: discord.abc.Messageable, user: Union[discord.User, discord.Member], when: datetime.datetime):

    for module in Modules.MODULES:
        if Utils.EVENT.on_typing in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_typing, channel, user, when))


@client.event
async def on_message(message: discord.Message):

    if message.content.startswith(Prefix):
        if message.content.split()[0] == f"{Prefix}help" or message.content.split()[0] == f"{Prefix}h":

            embed = discord.Embed()
            embed.set_footer(text=f"requested by {message.author}", icon_url=message.author.avatar_url)
            _module = ""

            if len(message.content.split()) == 2:
                found = False
                for module in Modules.MODULES:
                    if message.content.split()[1] == module:
                        found = True
                        _module = module
                        break
                    else:
                        for alias in Modules.libs[module].ALIASES:
                            if message.content.split()[1] == alias:
                                found = True
                                _module = module
                                break
                        if found:
                            break

                if not found:
                    embed.title = "**__:x: invalid cmd__**"
                    embed.add_field(name="", value=f"`{message.content.split()[1]}` isn't a cmd...")

                else:
                    embed.title = f"**__help: {message.content.split()[1]}__**"
                    embed.add_field(name=_module, value=f"""
Aliases: {Modules.libs[_module].ALIASES}
~~--------~~
{Modules.libs[_module].HELP.direct_help}
""")

            else:
                embed.title = "**__help | h__**"
                embed.add_field(name="better help:", value=f"> {Prefix}help NAME", inline=False)

                for module in Modules.MODULES:
                    if Utils.EVENT.on_message in Modules.libs[module].EVENTS:
                        if not Modules.libs[module].HELP.vanish:
                            _ = ""
                            for alias in Modules.libs[module].ALIASES:
                                _ += f"  **|** _{Prefix}{alias}_"
                            embed.add_field(name=f"_{Prefix}{module}_{_}", value=f"{Modules.libs[module].HELP}\n\n")

            create_task(message.channel.send(embed=embed))

        else:
            for module in Modules.MODULES:
                if Utils.EVENT.on_message in Modules.libs[module].EVENTS:
                    if message.content.split()[0] == f"{Prefix}{module}" or Modules.libs[module].HELP.order_2004:
                        create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_message, message))

                    else:
                        for alias in Modules.libs[module].ALIASES:
                            if message.content.split()[0] == f"{Prefix}{alias}":
                                create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_message, message))
                                break

    elif message.content.replace("!", "") == client.user.mention:
        create_task(message.channel.send(f"My Prefix is `{Prefix}`."))

    else:
        for module in Modules.MODULES:
            if Modules.libs[module].HELP.order_1793 or Modules.libs[module].HELP.order_2004:
                create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_message, message))


@client.event
async def on_message_delete(message: discord.Message):

    for module in Modules.MODULES:
        if Utils.EVENT.on_message_delete in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_message_delete, message))


@client.event
async def on_bulk_message_delete(messages: List[discord.Message]):

    for module in Modules.MODULES:
        if Utils.EVENT.on_bulk_message_delete in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_bulk_message_delete, messages))


@client.event
async def on_raw_message_delete(payload: discord.RawMessageDeleteEvent):

    for module in Modules.MODULES:
        if Utils.EVENT.on_raw_message_delete in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_raw_message_delete, payload))


@client.event
async def on_message_edit(before: discord.Message, after: discord.Message):

    for module in Modules.MODULES:
        if Utils.EVENT.on_message_edit in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_message_edit, before, after))


@client.event
async def on_raw_message_edit(payload: discord.RawMessageUpdateEvent):

    for module in Modules.MODULES:
        if Utils.EVENT.on_raw_message_edit in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_raw_message_edit, payload))


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: Union[discord.Member, discord.User]):

    for module in Modules.MODULES:
        if Utils.EVENT.on_reaction_add in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_reaction_add, reaction, user))


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):

    for module in Modules.MODULES:
        if Utils.EVENT.on_raw_reaction_add in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_raw_reaction_add, payload))


@client.event
async def on_reaction_remove(reaction: discord.Reaction, user: Union[discord.Member, discord.User]):

    for module in Modules.MODULES:
        if Utils.EVENT.on_reaction_remove in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_reaction_remove, reaction, user))


@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):

    for module in Modules.MODULES:
        if Utils.EVENT.on_raw_reaction_remove in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_raw_reaction_remove, payload))


@client.event
async def on_reaction_clear(message: discord.Message, reactions: List[discord.Reaction]):

    for module in Modules.MODULES:
        if Utils.EVENT.on_reaction_clear in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_reaction_clear, message, reactions))


@client.event
async def on_raw_reaction_clear(payload: discord.RawReactionClearEvent):

    for module in Modules.MODULES:
        if Utils.EVENT.on_raw_reaction_clear in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_raw_reaction_clear, payload))


@client.event
async def on_reaction_clear_emoji(reaction: discord.Reaction):

    for module in Modules.MODULES:
        if Utils.EVENT.on_reaction_clear_emoji in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_reaction_clear_emoji, reaction))


@client.event
async def on_raw_reaction_clear_emoji(payload: discord.RawReactionClearEmojiEvent):

    for module in Modules.MODULES:
        if Utils.EVENT.on_raw_reaction_clear_emoji in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_raw_reaction_clear_emoji, payload))


@client.event
async def on_private_channel_delete(channel: discord.abc.PrivateChannel):

    for module in Modules.MODULES:
        if Utils.EVENT.on_private_channel_delete in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_private_channel_delete, channel))


@client.event
async def on_private_channel_create(channel: discord.abc.PrivateChannel):

    for module in Modules.MODULES:
        if Utils.EVENT.on_private_channel_create in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_private_channel_create, channel))


@client.event
async def on_private_channel_update(before: discord.GroupChannel, after: discord.GroupChannel):

    for module in Modules.MODULES:
        if Utils.EVENT.on_private_channel_update in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_private_channel_update, before, after))


@client.event
async def on_private_channel_pins_update(channel: discord.abc.PrivateChannel, last_pin: Optional[datetime.datetime]):

    for module in Modules.MODULES:
        if Utils.EVENT.on_private_channel_pins_update in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_private_channel_pins_update, channel, last_pin))


@client.event
async def on_guild_channel_delete(channel: discord.abc.GuildChannel):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_channel_delete in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_channel_delete, channel))


@client.event
async def on_guild_channel_create(channel: discord.abc.GuildChannel):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_channel_create in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_channel_create, channel))


@client.event
async def on_guild_channel_update(before: discord.GroupChannel, after: discord.GroupChannel):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_channel_update in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_channel_update, before, after))


@client.event
async def on_guild_channel_pins_update(channel: discord.abc.PrivateChannel, last_pin: Optional[datetime.datetime]):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_channel_pins_update in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_channel_pins_update, channel, last_pin))


@client.event
async def on_guild_integrations_update(guild: discord.Guild):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_integrations_update in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_integrations_update, guild))


@client.event
async def on_webhooks_update(channel: discord.abc.GuildChannel):

    for module in Modules.MODULES:
        if Utils.EVENT.on_webhooks_update in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_webhooks_update, channel))


@client.event
async def on_member_join(member: discord.Member):

    for module in Modules.MODULES:
        if Utils.EVENT.on_member_join in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_member_join, member))


@client.event
async def on_member_remove(member: discord.Member):

    for module in Modules.MODULES:
        if Utils.EVENT.on_member_remove in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_member_remove, member))


@client.event
async def on_member_update(before: discord.Member, after: discord.Member):

    for module in Modules.MODULES:
        if Utils.EVENT.on_member_update in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_member_update, before, after))


@client.event
async def on_user_update(before: discord.User, after: discord.User):

    for module in Modules.MODULES:
        if Utils.EVENT.on_user_update in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_user_update, before, after))


@client.event
async def on_guild_join(guild: discord.Guild):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_join in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_join, guild))


@client.event
async def on_guild_remove(guild: discord.Guild):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_remove in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_remove, guild))


@client.event
async def on_guild_update(before: discord.Guild, after: discord.Guild):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_update in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_update, before, after))


@client.event
async def on_guild_role_create(role: discord.Role):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_role_create in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_role_create, role))


@client.event
async def on_guild_role_delete(role: discord.Role):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_role_delete in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_role_delete, role))


@client.event
async def on_guild_role_update(before: discord.Role, after: discord.Role):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_role_update in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_role_update, before, after))


@client.event
async def on_guild_emojis_update(guild: discord.Guild, before: Sequence[discord.Emoji], after: Sequence[discord.Emoji]):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_emojis_update in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_emojis_update, guild, before, after))


@client.event
async def on_guild_available(guild: discord.Guild):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_available in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_available, guild))


@client.event
async def on_guild_unavailable(guild: discord.Guild):

    for module in Modules.MODULES:
        if Utils.EVENT.on_guild_unavailable in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_guild_unavailable, guild))


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):

    for module in Modules.MODULES:
        if Utils.EVENT.on_voice_state_update in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_voice_state_update, member, before, after))


@client.event
async def on_member_ban(guild: discord.Guild, user: Union[discord.User, discord.Member]):

    for module in Modules.MODULES:
        if Utils.EVENT.on_member_ban in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_member_ban, guild, user))


@client.event
async def on_member_unban(guild: discord.Guild, user: discord.User):

    for module in Modules.MODULES:
        if Utils.EVENT.on_member_unban in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_member_unban, guild, user))


@client.event
async def on_invite_create(invite: discord.Invite):

    for module in Modules.MODULES:
        if Utils.EVENT.on_invite_create in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_invite_create, invite))


@client.event
async def on_invite_delete(invite: discord.Invite):

    for module in Modules.MODULES:
        if Utils.EVENT.on_invite_delete in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_invite_delete, invite))


@client.event
async def on_group_join(channel: discord.GroupChannel, user: discord.User):

    for module in Modules.MODULES:
        if Utils.EVENT.on_group_join in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_group_join, channel, user))


@client.event
async def on_group_remove(channel: discord.GroupChannel, user: discord.User):

    for module in Modules.MODULES:
        if Utils.EVENT.on_group_remove in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_group_remove, channel, user))


@client.event
async def on_relationship_add(relationship: discord.Relationship):

    for module in Modules.MODULES:
        if Utils.EVENT.on_relationship_add in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_relationship_add, relationship))


@client.event
async def on_relationship_remove(relationship: discord.Relationship):

    for module in Modules.MODULES:
        if Utils.EVENT.on_relationship_remove in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_relationship_remove, relationship))


@client.event
async def on_relationship_update(before: discord.Relationship, after: discord.Relationship):

    for module in Modules.MODULES:
        if Utils.EVENT.on_relationship_update in Modules.libs[module].EVENTS:

            create_task(Modules.libs[module].__main__(client, Utils.EVENT.on_relationship_update, before, after))


client.run(TOKEN, intents=discord.Intents.all())
