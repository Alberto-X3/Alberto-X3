import discord
import Utils


HELP = Utils.Help(vanish=True, order_1793=True)
EVENTS = [Utils.EVENT.on_message, Utils.EVENT.on_message_delete, Utils.EVENT.on_message_edit]


async def __main__(client: discord.Client, _event: int, *args: Utils.Optional[discord.Message]):
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

        else:
            embed = discord.Embed()

        await super_log.send(embed=embed, files=attachments)

    except Exception as e:
        import datetime
        super_log: discord.TextChannel = client.get_channel(Utils.DATA.IDs.Channels.Super_Log)

        embed: discord.Embed = discord.Embed(title=__name__,
                                             description=f"{e.__class__.__name__}: {e.__str__()}\n",
                                             color=discord.Color.magenta())

        embed.add_field(name="datetime.datetime",
                        value=datetime.datetime.utcnow().isoformat().replace("T", ""))

        await super_log.send(embed=embed)
