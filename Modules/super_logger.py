import discord
import Utils


HELP = Utils.Help(vanish=True, order_2004=True)
EVENTS = [
    Utils.EVENT.on_message,
    Utils.EVENT.on_message_delete,
    Utils.EVENT.on_message_edit,
    Utils.EVENT.on_ready,
    Utils.EVENT.on_voice_state_update
]


async def __main__(client: discord.Client, _event: int, *args: Utils.Union[discord.Message, discord.Member, discord.VoiceState]):
    try:
        super_log: discord.TextChannel = client.get_channel(Utils.DATA.IDs.Channels.Super_Log)
        attachments = None

        if _event == Utils.EVENT.on_message:

            if args[0].channel.id != super_log.id:
                embed: discord.Embed = discord.Embed(title=f"on_message | <{args[0].jump_url}>",
                                                     description=args[0].content,
                                                     color=discord.Color.gold())
                embed.set_author(name=args[0].author, url=args[0].author.avatar_url)
                embed.add_field(name="datetime.datetime",
                                value=args[0].created_at)

                from io import BytesIO
                if args[0].attachments:
                    attachments = []
                    for attachment in args[0].attachments:
                        fp = BytesIO()
                        await attachment.save(fp)
                        attachments += [discord.File(fp, attachment.filename)]
            else:
                return

        elif _event == Utils.EVENT.on_message_delete:
            embed: discord.Embed = discord.Embed(title=f"on_message_delete | <{args[0].jump_url}>",
                                                 description=args[0].content+" ",
                                                 color=discord.Color.gold())
            embed.set_author(name=args[0].author, url=args[0].author.avatar_url)
            embed.add_field(name="datetime.datetime",
                            value=args[0].created_at)

        elif _event == Utils.EVENT.on_message_edit:
            if args[0].author.id != client.user.id:
                embed: discord.Embed = discord.Embed(title=f"on_message_edit | <{args[0].jump_url}>",
                                                     color=discord.Color.gold())
                embed.set_author(name=args[0].author, url=args[0].author.avatar_url)
                embed.add_field(name=f"before ({args[0].created_at})",
                                value=args[0].content+" ")
                embed.add_field(name=f"after ({args[0].edited_at})",
                                value=args[1].content+" ")
            else:
                return

        elif _event == Utils.EVENT.on_ready:
            embed: discord.Embed = discord.Embed(title=f"on_ready",
                                                 color=discord.Color.green())

        elif _event == Utils.EVENT.on_voice_state_update:
            embed: discord.Embed = discord.Embed(title=f"on_voice_state_update",
                                                 color=discord.Color.greyple())
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

        else:
            embed = discord.Embed()

        await super_log.send(embed=embed, files=attachments)

    except Exception as e:
        from discord.utils import snowflake_time

        super_log: discord.TextChannel = client.get_channel(Utils.DATA.IDs.Channels.Super_Log)
        embed: discord.Embed = discord.Embed(title=__name__,
                                             description=f"{e.__class__.__name__}: {e.__str__()}\n",
                                             color=discord.Color.magenta())

        message: discord.Message = await super_log.send(embed=embed)

        embed.add_field(name="datetime.datetime",
                        value=snowflake_time(message.id).__str__())
        await message.edit(embed=embed)
        await message.pin()
        await super_log.send(f"<@&{820974562770550816}>", delete_after=0)
