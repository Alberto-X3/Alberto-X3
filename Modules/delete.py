import discord
import Utils


HELP = Utils.Help("deletes the amount of messages (max 99)", f"_{Utils.Prefix}delete iD (reason)_")
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["del"]


async def __main__(client: discord.Client, _event: int, message: discord.Message):
    user_perms = Utils.perms(str(message.author.id))

    if user_perms.Admin.delete:
        if len(message.content.split(" ")) == 2:
            if message.content.split(" ")[1].isnumeric():
                await message.delete()

                limit = 99
                if 0 < int(message.content.split()[1]) < limit:
                    limit = int(message.content.split()[1])

                log = await message.channel.purge(limit=limit, check=lambda msg_: not msg_.pinned)
                channel_for_logging = await client.fetch_channel(Utils.DATA.IDs.Channels.Logs)
                await Utils.Logger(channel_for_logging).delete(user=message.author, count=len(log), channel=message.channel)

                super_log: discord.TextChannel = client.get_channel(Utils.DATA.IDs.Channels.Super_Log)

                embed = discord.Embed(title=f"#{message.channel}", color=discord.Color(Utils.DATA.colors.red))
                embed.set_author(name=f"{message.author}", icon_url=message.author.avatar_url)
                for msg in log[::-1]:
                    msg: discord.Message

                    await super_log.trigger_typing()

                    content = f"{msg.content}"
                    embed.add_field(name=f"{msg.author} | {msg.author.id}, {msg.created_at}", value=content if content else f"***__EMBED__***", inline=False)

                await super_log.send(embed=embed)
