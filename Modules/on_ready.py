import discord
import Utils

from typing import List
from asyncio import sleep
from datetime import datetime, timedelta
from aiohttp import ClientSession


EVENTS = [Utils.EVENT.on_ready]


async def __main__(client: discord.Client, _event: int):

    try:
        print(f"Logged in as {client.user}")
        await client.change_presence(activity=discord.Activity(name=f"{Utils.Prefix}help", type=discord.ActivityType.listening), status=discord.Status.online)

        ...

        id_channel: int = 808742319066579014
        id_message: int = 809048308358184981

        channel: discord.TextChannel = client.get_channel(id_channel)
        message: discord.Message = await channel.fetch_message(id_message)

        tag_cases = b"<h1>Coronavirus Cases:</h1>"
        tag_deaths = b"<h1>Deaths:</h1>"
        tag_recovered = b"<h1>Recovered:</h1>"

        tag_end = b"</span>"

        url = r"https://www.worldometers.info/coronavirus/"

        dis_cases = 86
        dis_deaths = 56
        dis_recovered = 82

        first = True
        old_list_cases = []
        old_list_deaths = []
        old_list_recovered = []
        old_list_active = []

        async with ClientSession() as session:
            while True:
                try:
                    resp = session.get(url)
                    data = await resp
                    content = await data.read()

                    pos_cases = content.find(tag_cases)
                    pos_deaths = content.find(tag_deaths)
                    pos_recovered = content.find(tag_recovered)

                    cases = content[pos_cases+dis_cases:pos_cases+dis_cases+content[pos_cases+dis_cases:].find(tag_end)]
                    deaths = content[pos_deaths+dis_deaths:pos_deaths+dis_deaths+content[pos_deaths+dis_deaths:].find(tag_end)]
                    if deaths.startswith(b">"):
                        deaths = content[pos_deaths+dis_deaths+1:pos_deaths+dis_deaths+1+content[pos_deaths+dis_deaths+1:].find(tag_end)]
                    recovered = content[pos_recovered+dis_recovered:pos_recovered+dis_recovered+content[pos_recovered+dis_recovered:].find(tag_end)]

                    cases = cases.replace(b" ", b"")
                    deaths = deaths.replace(b" ", b"")
                    recovered = recovered.replace(b" ", b"")

                    int_cases = int(cases.replace(b",", b""))
                    int_deaths = int(deaths.replace(b",", b""))
                    int_recovered = int(recovered.replace(b",", b""))

                    int_active = int_cases - int_deaths - int_recovered
                    active = ("".join(str(int_active)[::-1][i]+"," if i % 3 == 2 else str(int_active)[::-1][i] for i in range(len(str(int_active)))))[::-1]
                    if active.startswith(","):
                        active = active[1:]

                    history = len(old_list_cases)

                    old_list_cases = ut(old_list_cases, int_cases)
                    old_list_deaths = ut(old_list_deaths, int_deaths)
                    old_list_recovered = ut(old_list_recovered, int_recovered)
                    old_list_active = ut(old_list_active, int_active)

                    new_cases = dif(old_list_cases)
                    new_deaths = dif(old_list_deaths)
                    new_recovered = dif(old_list_recovered)
                    new_active = dif(old_list_active)

                    if first:
                        first = False

                    msg = f"""
__**🌐 World Wide**__
```md
COVID-19 Cases
------------------------
{cases.decode():13}{
    ('-' if new_cases < 0 else '+')+str(abs(new_cases)):7}

Deaths
------------------------
{deaths.decode():13}{
    ('-' if new_deaths < 0 else '+') + str(abs(new_deaths)):7}

Recovered
------------------------
{recovered.decode():13}{
    ('-' if new_recovered < 0 else '+') + str(abs(new_recovered)):7}

Active
------------------------
{active:13}{
    ('-' if new_active < 0 else '+') + str(abs(new_active)):7}

> UTC {datetime.utcnow().date()} {datetime.utcnow().hour}:{"0"+str(datetime.utcnow().minute) if datetime.utcnow().minute < 10 else datetime.utcnow().minute}```
@here is the source: <{url}> :)
[`+`/`-` are the differences from the past {history} minutes]
"""

                    await message.edit(content=msg)

                    await sleep((timedelta(minutes=1)-timedelta(seconds=datetime.utcnow().second, microseconds=datetime.utcnow().microsecond)).total_seconds())

                except (KeyError, IndexError, ValueError, TypeError,
                        AttributeError, RuntimeError):
                    pass

    except Exception as e:
        await Utils.send_exception(client=client, exception=e, source_name=__name__)


def dif(obj: List[int]) -> int:
    if len(obj) <= 1:
        return 0
    return obj[0] - obj[-1]


def update_timeline(obj: List[int], value: int,
                    max_len: int = 10) -> List[int]:
    obj.insert(0, value)
    return obj[:max_len]


ut = update_timeline
