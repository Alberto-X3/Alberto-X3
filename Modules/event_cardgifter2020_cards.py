import discord
import Utils


HELP = Utils.Help(order_2004=True, vanish=True)
EVENTS = [Utils.EVENT.on_message]
ALIASES = []


async def __main__(client: discord.Client, _event: int, message: discord.Message):
    try:
        if message.channel.id != 821843251195412530:
            return

        log: discord.TextChannel = client.get_channel(821845250451439636)

        await log.send(f"__{message.author.mention}__\n"
                       f"```\n{message.content}\n```\n"
                       f"{message.author.avatar_url}")

        await message.add_reaction("✅")

    except Exception as e:
        await Utils.send_exception(client=client, exception=e, source_name=__name__)
