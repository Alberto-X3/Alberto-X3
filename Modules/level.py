from discord import Embed, Client, Message, Role, NotFound, Member, User
from Utils import Help, EVENT, send_exception, Prefix

from sqlite3 import connect
from random import choice
from typing import Tuple, Dict, Union
from datetime import datetime, timedelta

HELP = Help("shows you your XP", f"{Prefix}level (iD/ping)", order_1793=True)
EVENTS = [EVENT.on_message]
ALIASES = ["lvl", "rank"]

possible_xps = [2, 2,
                3, 3, 3, 3,
                4, 4, 4,
                5, 5]
free = "<:XP0:831578582026813480>"
full = "<:XP1:831578621092691978>"
len_bar = 20
formula = 1 / 3
latency = timedelta(minutes=1)

lvl_rewards = {
    "25": 831628612171071498,
    "20": 831628364803997757,
    "15": 831628201406627871,
    "10": 831628459222237227,
    "5": 831915216475914273
}
recent: Dict[int, datetime] = {}

needed = {
    # 1: 8,
    # 2: 27,
    # 3: 65,
    # 4: 125,
    5: 217,
    # 6: 344,
    # 7: 513,
    # 8: 730,
    # 9: 1001,
    10: 1332,
    # 11: 1729,
    # 12: 2198,
    # 13: 2745,
    # 14: 3376,
    15: 4097,
    # 16: 4914,
    # 17: 5833,
    # 18: 6860,
    # 19: 8001,
    20: 9262,
    # 21: 10649,
    # 22: 12168,
    # 23: 13825,
    # 24: 15626,
    25: 17577,
    # 26: 19684,
    # 27: 21953,
    # 28: 24390,
    # 29: 27001,
    30: 29792,
    # 31: 32769,
    # 32: 35938,
    # 33: 39305,
    # 34: 42876,
    35: 46657,
    # 36: 50654,
    # 37: 54873,
    # 38: 59320,
    # 39: 64001,
    40: 68922
}
needed_info = """```
Level:  XP:
{}
```""".format("\n".join(f"{str(k):8}{needed[k]}" for k in list(needed)))


async def __main__(client: Client, _event: int, message: Message):
    try:
        if message.guild is None:
            return

        try:
            user = int(message.content.split()[-1].replace("<", "")
                       .replace("@", "")
                       .replace("!", "")
                       .replace(">", ""))
            message.author = await client.fetch_user(user)
        except (ValueError, NotFound, IndexError):
            user = message.author.id

        db = connect("levels.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM lvl WHERE user=={user}")

        fetched = cursor.fetchone()
        if fetched is None:
            cursor.execute(f"INSERT INTO lvl VALUES ({user}, 0, 0)")
            db.commit()

        data: Tuple[int, int, int] = fetched or (user, 0, 0)

        cursor.execute("SELECT * from lvl ORDER BY xp DESC LIMIT 10")
        rank = cursor.fetchall()

        ranking = {
            "inline": False,
            "name": f"__Ranking #{len(rank)}:__",
            "value": "\n".join(f"LVL **{l}**; "
                               f"XP **{x}**; "
                               f"<@{u}>" for u, l, x in rank)
        }

        cursor.execute("SELECT null from lvl")
        len_user = len(cursor.fetchall())

        xp = data[2]
        lvl = data[1]

        if message.content.startswith(("!!", "++", "..", "??")):
            """
            `!!` -> prefix for <@714477299042615361> (Josef#0189)
            `++` -> prefix for <@772085213987209226> (Red-Rainbow#0836)
            `..` -> prefix for <@751157545728606239> (Alberto-X3#9164)
            `??` -> prefix for <@756196727748296855> (CardGifter2020#2871)
            """
            if not message.content.startswith(".."):
                return

            user_level = xp ** formula
            user_progress = int(str(user_level).split(".")[1][:2])
            len_filled = int(len_bar * user_progress / 100)

            bar = f"{'#' * len_filled:-<{len_bar}}"
            bar = bar.replace("#", full)
            bar = bar.replace("-", free)

            cursor.execute(f"SELECT level FROM lvl where xp>{xp}")
            rank = len(cursor.fetchall()) + 1

            embed = Embed(color=0x275591,
                          description=f"You are the number __**#{rank}**__ {message.author.mention}!")
            embed.set_author(name=message.author.name,
                             icon_url=message.author.avatar_url)
            embed.set_footer(text=f"total {len_user} user in ranking")

            embed.add_field(inline=False,
                            name="__Your LVL:__", value=str(lvl))
            embed.add_field(inline=False,
                            name="__Your XP:__", value=f"{xp}\n{bar}")
            embed.add_field(**ranking)
            embed.add_field(name="__Info:__", value=needed_info, inline=False)

            await message.channel.send(embed=embed)
            return

        # below is only without prefix and just leveling
        if message.channel.slowmode_delay:
            return

        author: Member = message.guild.get_member(message.author.id)

        try:
            if recent[user] + latency > datetime.utcnow():
                if not message.content.startswith("\u200B"):
                    if recent[user] + latency / 2 > datetime.utcnow():
                        return
                else:
                    return
        except KeyError:
            pass

        recent[user] = datetime.utcnow()

        xp += choice(possible_xps)
        old_lvl = lvl
        lvl = int(xp ** formula) - 1

        cursor.execute(f"UPDATE lvl SET level={lvl} WHERE user=={user}")
        cursor.execute(f"UPDATE lvl SET xp={xp} WHERE user=={user}")

        db.commit()
        db.close()

        if lvl != old_lvl:
            await client.get_channel(831625194803298314).send(
                f"Congratulations __**{message.author.mention}**__!\n"
                f"You are now __*Level {lvl}*__ 🥳🥳🥳\n")

            if str(lvl) in lvl_rewards:
                reward: Role = message.guild.get_role(lvl_rewards[str(lvl)])
                await author.add_roles(reward, reason="Leveling reward")

    except Exception as e:
        await send_exception(client=client, exception=e, source_name=__name__)
