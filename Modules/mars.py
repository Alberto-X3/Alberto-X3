from aiohttp import ClientSession, ClientResponse
from discord import Client, Message, Embed
from datetime import datetime, timedelta
from asyncio import sleep as asleep
import Utils


HELP = Utils.Help("shows latest pictures from Mars")
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["m"]

LOADING_MSG = "<a:loading:832383867700772866> loading `api.nasa.gov`..."
API_KEY = Utils.DATA.CONSTANTS.KEY_01
BASE_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos" \
           "?earth_date={date}&api_key=" + API_KEY
MAX_HISTORY: int = 4


def get_date(history) -> str:
    """returns the date for the images"""
    return (datetime.utcnow()-timedelta(days=history)).strftime("%Y-%m-%d")


async def __main__(client: Client, _event: int, message: Message):
    try:
        message: Message = await message.channel.send(LOADING_MSG)

        data = []
        async with ClientSession() as session:
            for history in range(1, MAX_HISTORY+1):
                url = BASE_URL.format(date=get_date(history))

                resp: ClientResponse = await (session.get(url))
                data += (await resp.json())["photos"]

        # I convert the images and sols to a set to prevent multiplying
        images_set = {(i["img_src"], i["sol"])
                      for i in data if "/ncam/" in i["img_src"]}
        del data

        images = [*sorted(images_set, key=lambda t: t[1], reverse=True)]
        del images_set

        for image in images:
            embed: Embed = Embed(title=f"Mars Sol {image[1]}",
                                 description="Recent images from Mars!")
            embed.set_image(url=image[0])
            await message.edit(embed=embed, content="")
            await asleep(10)
        del images

        await message.edit(content=f"To restart the slide-show type "
                                   f"`{Utils.Prefix}{__name__.split('.')[-1]}`")

    except Exception as e:
        await Utils.send_exception(client=client, exception=e, source_name=__name__)
