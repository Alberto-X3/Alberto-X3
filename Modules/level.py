from discord import Embed, Client, Message
from Utils import Help, EVENT, send_exception, DATA

from sqlite3 import connect
from random import choice
from typing import Tuple


HELP = Help("shows you your XP", order_1793=True)
EVENTS = [EVENT.on_message]
ALIASES = ["lvl", "rank"]

possible_xps = [3, 3,
                4, 4, 4, 4,
                5, 5, 5,
                6, 6,
                7]
free = "<:XP0:831578582026813480>"
full = "<:XP1:831578621092691978>"
len_bar = 20
formula = 1/4.5


async def __main__(client: Client, _event: int, message: Message):
    try:
        if any((message.author.bot,
                message.guild is None)):
            return

        user = message.author.id

        db = connect("levels.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM lvl WHERE user=={user}")

        fetched = cursor.fetchone()
        if fetched is None:
            cursor.execute(f"INSERT INTO lvl VALUES ({user}, 0, 0)")
            db.commit()

        data: Tuple[int, int, int] = fetched or (user, 0, 0)

        xp = data[2]
        lvl = data[1]

        if message.content.startswith(DATA.CONSTANTS.Prefix):
            user_level = xp ** formula
            user_progress = int(str(user_level).split(".")[1][:2])
            len_filled = int(len_bar*user_progress/100)

            bar = f"{'#' * len_filled:-<{len_bar}}"
            bar = bar.replace("#", full)
            bar = bar.replace("-", free)

            embed: Embed = Embed(color=0x275591)
            embed.set_author(name=message.author.name,
                             icon_url=message.author.avatar_url)

            embed.add_field(inline=False,
                            name="Your LVL:", value=str(lvl))
            embed.add_field(inline=False,
                            name="Your XP:", value=f"{xp}\n{bar}")

            await message.channel.send(embed=embed)
            return

        # below is only without prefix and just leveling

        xp += choice(possible_xps)

        if lvl < int(xp ** formula) - 1:
            lvl = int(xp ** formula) - 1
            await client.get_channel(831625194803298314).send(
                f"Congratulations __**{message.author.mention}**__!\n"
                f"You are now __*Level {lvl}*__ 🥳🥳🥳\n")

        cursor.execute(f"UPDATE lvl SET level={lvl} WHERE user=={user}")
        cursor.execute(f"UPDATE lvl SET xp={xp} WHERE user=={user}")

        db.commit()
        db.close()

    except Exception as e:
        await send_exception(client=client, exception=e, source_name=__name__)
