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
formula = 1/3
latency = timedelta(minutes=1)

lvl_rewards = {
    "25": 831628612171071498,
    "20": 831628364803997757,
    "15": 831628201406627871,
    "10": 831628459222237227,
    "5":  831915216475914273
}
recent: Dict[int, datetime] = {}


async def __main__(client: Client, _event: int, message: Message):
    try:
        if any((message.author.bot,
                message.guild is None)):
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
        print(rank)
        ranking = {"inline": False,
                   "name": f"__Ranking #{len(rank)}:__",
                   "value": "\n".join(f"LVL **{l}**; "
                                      f"XP **{x}**; "
                                      f"<@{u}>" for u, l, x in rank)}

        xp = data[2]
        lvl = data[1]

        if message.content.startswith(Prefix):
            user_level = xp ** formula
            user_progress = int(str(user_level).split(".")[1][:2])
            len_filled = int(len_bar*user_progress/100)

            bar = f"{'#' * len_filled:-<{len_bar}}"
            bar = bar.replace("#", full)
            bar = bar.replace("-", free)

            cursor.execute(f"SELECT level FROM lvl where xp>{xp}")
            rank = len(cursor.fetchall()) + 1

            embed = Embed(color=0x275591,
                          description=f"You are the number __**#{rank}**__!")
            embed.set_author(name=message.author.name,
                             icon_url=message.author.avatar_url)

            embed.add_field(inline=False,
                            name="__Your LVL:__", value=str(lvl))
            embed.add_field(inline=False,
                            name="__Your XP:__", value=f"{xp}\n{bar}")
            embed.add_field(**ranking)

            await message.channel.send(embed=embed)
            return

        # below is only without prefix and just leveling
        author: Union[Member, User] = message.author

        try:
            if recent[user]+latency > datetime.utcnow():
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
