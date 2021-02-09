import discord
import Utils

from asyncio import sleep
from datetime import datetime
import requests


EVENTS = [Utils.EVENT.on_ready]


async def __main__(client: discord.Client, _event: int):

    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Activity(name=f"{Utils.Prefix}help", type=discord.ActivityType.listening), status=discord.Status.online)

    ...

    id_channel: int = 808742319066579014
    id_message: int = 808743419768995920

    channel: discord.TextChannel = client.get_channel(id_channel)
    message: discord.Message = await channel.fetch_message(id_message)

    tag_cases = b"<h1>Coronavirus Cases:</h1>"
    tag_deaths = b"<h1>Deaths:</h1>"
    tag_recovered = b"<h1>Recovered:</h1>"

    tag_end = b"</span>"

    dis_cases = 86
    dis_deaths = 56
    dis_recovered = 82

    first = True
    old_int_cases = old_int_deaths = old_int_recovered = old_int_active = -1
    while True:

        data: requests.Response = requests.get(r"https://www.worldometers.info/coronavirus/")

        pos_cases = data.content.find(tag_cases)
        pos_deaths = data.content.find(tag_deaths)
        pos_recovered = data.content.find(tag_recovered)

        cases = data.content[pos_cases+dis_cases:pos_cases+dis_cases+data.content[pos_cases+dis_cases:].find(tag_end)]
        deaths = data.content[pos_deaths+dis_deaths:pos_deaths+dis_deaths+data.content[pos_deaths+dis_deaths:].find(tag_end)]
        if deaths.startswith(b">"):
            deaths = data.content[pos_deaths+dis_deaths+1:pos_deaths+dis_deaths+1+data.content[pos_deaths+dis_deaths+1:].find(tag_end)]
        recovered = data.content[pos_recovered+dis_recovered:pos_recovered+dis_recovered+data.content[pos_recovered+dis_recovered:].find(tag_end)]

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

        msg = f"""
```md
COVID-19 Cases
------------------------
{cases.decode():11}{f" < +{int_cases-old_int_cases:5} >" if int_cases-old_int_cases and not first else ""}

Deaths
------------------------
{deaths.decode():11}{f" < +{int_deaths-old_int_deaths:5} >" if int_deaths-old_int_deaths and not first else ""}

Recovered
------------------------
{recovered.decode():11}{f" < +{int_recovered-old_int_recovered:5} >" if int_recovered-old_int_recovered and not first else ""}

Active
------------------------
{active:11}{f" < {'+' if int_active-old_int_active > 0 else '-'}{abs(int_active-old_int_active):5} >" if int_active-old_int_active and not first else ""}

> {datetime.now().date()} {datetime.now().hour}:{"0"+str(datetime.now().minute) if datetime.now().minute < 10 else datetime.now().minute}```
coded by <@{Utils.DATA.Author_id}> for @here :)
"""

        await message.edit(content=msg)

        old_int_cases = int_cases
        old_int_deaths = int_deaths
        old_int_recovered = int_recovered
        old_int_active = int_active

        if first:
            first = False

        await sleep(60)
