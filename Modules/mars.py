from aiohttp import ClientSession, ClientResponse
from discord import Client, Message, Embed
from datetime import datetime, timedelta
from typing import Dict, List, Union
from asyncio import sleep as asleep
import Utils


HELP = Utils.Help("shows latest pictures from Mars")
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["m"]

LOADING_MSG = "<a:loading:832383867700772866> loading `api.nasa.gov`..."
API_KEY = Utils.DATA.CONSTANTS.KEY_01
BASE_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos" \
           "?earth_date={date}&api_key=" + API_KEY
_DATA_T = \
    Dict[
        str, List[
            Dict[
                str, Union[str, int, Dict[
                    str, Union[str, int]]
                ]
            ]
        ]
    ]


async def __main__(client: Client, _event: int, message: Message):
    try:
        url = BASE_URL.format(date=(datetime.utcnow()-timedelta(days=1)).strftime("%Y-%m-%d"))

        message: Message = await message.channel.send(LOADING_MSG)

        async with ClientSession() as session:
            resp: ClientResponse = await (session.get(url))
            data: _DATA_T = await resp.json()

        images = [*{(i["img_src"], i["sol"]) for i in data["photos"]
                    if "/ncam/" in i["img_src"]}]

        for index in range(len(images)):
            embed: Embed = Embed(title=f"Mars Sol {images[index][1]}",
                                 description="Recent images from Mars!")
            embed.set_image(url=images[index][0])
            await message.edit(embed=embed, content="")
            await asleep(10)
        del images

        await message.edit(content=f"To restart the slide-show type "
                                   f"`{Utils.Prefix}{__name__.split('.')[-1]}`")

    except Exception as e:
        await Utils.send_exception(client=client, exception=e, source_name=__name__)
