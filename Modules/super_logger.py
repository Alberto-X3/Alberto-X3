from discord import Client, Message, Member, User, VoiceState, Role, TextChannel, Embed, Color, File
from Utils import Help, Union, EVENT, DATA


HELP = Help(vanish=True, order_2004=True)
EVENTS = [
    EVENT.on_message,
    EVENT.on_message_delete,
    EVENT.on_message_edit,
    EVENT.on_ready,
    EVENT.on_voice_state_update,
    EVENT.on_user_update,
    EVENT.on_member_update
]


async def __main__(client: Client, _event: int, *args: Union[Message, Member, VoiceState, User, Member, Role]):
    try:
        super_log: TextChannel = client.get_channel(DATA.IDs.Channels.Super_Log)
        attachments = None

        if _event == EVENT.on_message:
            datetime_edit = False

            if args[0].channel.id != super_log.id:
                embed: Embed = Embed(title=f"on_message | "
                                           f"<{args[0].jump_url}> |"
                                           f" {args[0].channel.category} |"
                                           f" {args[0].channel.mention}",
                                     description=args[0].content,
                                     color=Color.gold())
                embed.set_author(name=args[0].author, url=args[0].author.avatar_url)
                embed.add_field(name="datetime.datetime",
                                value=args[0].created_at)

                from io import BytesIO
                if args[0].attachments:
                    attachments = []
                    for attachment in args[0].attachments:
                        fp = BytesIO()
                        await attachment.save(fp)
                        attachments += [File(fp, attachment.filename)]
            else:
                return

        elif _event == EVENT.on_message_delete:
            datetime_edit = False
            embed: Embed = Embed(title=f"on_message_delete | "
                                       f"<{args[0].jump_url}> |"
                                       f" {args[0].channel.category} |"
                                       f" {args[0].channel.mention}",
                                 description=args[0].content+" ",
                                 color=Color.gold())
            embed.set_author(name=args[0].author, url=args[0].author.avatar_url)
            embed.add_field(name="datetime.datetime",
                            value=args[0].created_at)

        elif _event == EVENT.on_message_edit:
            datetime_edit = False
            if args[0].author.id != client.user.id:
                embed: Embed = Embed(title=f"on_message_edit | "
                                           f"<{args[0].jump_url}> |"
                                           f" {args[0].channel.category} |"
                                           f" {args[0].channel.mention}",
                                     color=Color.gold())
                embed.set_author(name=args[0].author, url=args[0].author.avatar_url)
                embed.add_field(name=f"before ({args[0].created_at})",
                                value=args[0].content+" ")
                embed.add_field(name=f"after ({args[0].edited_at})",
                                value=args[1].content+" ")
            else:
                return

        elif _event == EVENT.on_ready:
            datetime_edit = True
            embed: Embed = Embed(title=f"on_ready",
                                 color=Color.green())

        elif _event == EVENT.on_voice_state_update:
            datetime_edit = True
            embed: Embed = Embed(title=f"on_voice_state_update",
                                 color=Color.greyple())
            embed.set_author(name=args[0].__str__(), url=args[0].avatar_url)

            if args[1].channel is None:
                embed.description = f"joined {args[2].channel}"
            if args[2].channel is None:
                embed.description = f"leafed {args[1].channel}"
            if args[1].channel is not None and args[2].channel is not None and args[1].channel != args[2].channel:
                embed.add_field(name="moved", value=f"{args[1].channel} -> {args[2].channel}")
            if args[1].deaf != args[2].deaf:
                embed.add_field(name="server deafen", value=f"{args[1].deaf} -> {args[2].deaf}")
            if args[1].mute != args[2].mute:
                embed.add_field(name="server mute", value=f"{args[1].mute} -> {args[2].mute}")
            if args[1].self_deaf != args[2].self_deaf:
                embed.add_field(name="self self_deafen", value=f"{args[1].self_deaf} -> {args[2].self_deaf}")
            if args[1].self_mute != args[2].self_mute:
                embed.add_field(name="self mute", value=f"{args[1].self_mute} -> {args[2].self_mute}")
            if args[1].self_stream != args[2].self_stream:
                embed.add_field(name="self stream", value=f"{args[1].self_stream} -> {args[2].self_stream}")
            if args[1].self_video != args[2].self_video:
                embed.add_field(name="self video", value=f"{args[1].self_video} -> {args[2].self_video}")
            if args[1].afk != args[2].afk:
                embed.add_field(name="afk", value=f"{args[1].afk} -> {args[2].afk}")

        elif _event == EVENT.on_user_update:
            datetime_edit = True
            embed: Embed = Embed(title=f"on_user_update",
                                 color=Color.blurple())
            embed.set_author(name=args[0].__str__(), url=args[0].avatar_url)
            if args[0].avatar != args[1].avatar:
                embed.add_field(name="avatar", value=f"[IMG]({args[0].avatar_url}) -> [IMG]({args[1].avatar_url})")
            if args[0].name != args[1].name:
                embed.add_field(name="name", value=f"{args[0].name} -> {args[1].name}")
            if args[0].discriminator != args[1].discriminator:
                embed.add_field(name="discriminator", value=f"{args[0].discriminator} -> {args[1].discriminator}")

        elif _event == EVENT.on_member_update:
            datetime_edit = True
            embed: Embed = Embed(title=f"on_member_update",
                                 color=Color.blue())
            embed.set_author(name=args[0].__str__(), url=args[0].avatar_url)
            if args[0].nick != args[1].nick:
                embed.add_field(name="nickname", value=f"{args[0].nick} -> {args[1].nick}")
            if args[0].roles != args[1].roles:
                embed.add_field(name="roles", value=f"{args[0].roles} -> {args[1].roles}")

            if len(embed.fields) == 0:
                return

        else:
            datetime_edit = True
            embed = Embed()

        message: Message = await super_log.send(embed=embed, files=attachments)

        if datetime_edit:
            from discord.utils import snowflake_time
            embed.add_field(name="datetime.datetime",
                            value=snowflake_time(message.id).__str__(),
                            inline=False)
            await message.edit(embed=embed)

    except Exception as e:
        from discord.utils import snowflake_time

        super_log: TextChannel = client.get_channel(DATA.IDs.Channels.Super_Log)
        embed: Embed = Embed(title=__name__,
                             description=f"{e.__class__.__name__}: {e.__str__()}\n",
                             color=Color.magenta())

        message: Message = await super_log.send(embed=embed)

        embed.add_field(name="datetime.datetime",
                        value=snowflake_time(message.id).__str__())
        await message.edit(embed=embed)
        await message.pin()
        await super_log.send(f"<@&{820974562770550816}>", delete_after=0)
