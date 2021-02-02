import discord
import Utils

from os import listdir
from json import load

DATA = Utils.AttrDict(load(open("Configs.json")))
Prefix = DATA.CONSTANTS.Prefix
author = DATA.Author
author_id = DATA.Author_id

HELP = Utils.Help(f"vanish")
EVENTS = [Utils.EVENT.on_message]


async def __main__(client: discord.Client, _event: int, message: discord.Message):

    if message.author.id == author_id:
        if len(message.content.split(" ")) == 1:
            await message.author.send("""
Possible:

> _update_ <_-root_> **+** _File.py_
> _get_ _filename.py_ <_-root_>

> _system_
""")

        elif message.content.split(" ")[1] == "update":
            await update(message)

        elif message.content.split(" ")[1] == "get":
            await get(message)

        elif message.content.split(" ")[1] == "system":
            await system(message)

        else:
            ...

    else:
        await message.channel.send(f":x: **YOU ARE NOT {author}!!!**")


async def update(message: discord.Message):
    if message.attachments:

        if message.content.split(" ")[-1] == "-root":
            path = ""
        else:
            path = "Modules/"

        await message.attachments[0].save(f"./{path}{message.attachments[0].filename}")
        await message.author.send(f"__*{message.attachments[0].filename}*__ successfully added {'' if path else 'to root'}")

    else:
        await message.author.send("Please add a file...")


async def get(message: discord.Message):
    if len(message.content.split(" ")) == 3 or len(message.content.split(" ")) == 4:

        if message.content.split(" ")[-1] == "-root":
            path = ""
        else:
            path = "Modules/"

        if message.content.split(" ")[2] in listdir(f"./{path}"):
            await message.author.send(f"Here is your file {'' if path else 'from root'}...", file=discord.File(open(f"./{path}{message.content.split(' ')[2]}", "rb"), filename=message.content.split(' ')[2]))

        else:
            await message.author.send("Please name a valid filename...")
    else:
        await message.author.send("Please name a filename...")


async def system(message: discord.Message):
    log = {}
    from datetime import datetime
    import platform
    try: import psutil
    except ImportError:
        await message.author.send("`psutil` not found...")
    else:
        await message.author.trigger_typing()

        uname = platform.uname()
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        _1 = []
        for i, perc in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            _1 += [f"Core {i}: {perc}%"]
        virtual_mem = psutil.virtual_memory()

        def adjust_size(size):
            factor = 1024
            for short in ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "BB"]:
                if size > factor:
                    size = size / factor
                else:
                    return f"{size:.3f}{short}"

        swap = psutil.swap_memory()

        ...

        log["Sys Info"] = ""
        log["system"] = uname.system
        log["node name"] = uname.node
        log["release"] = uname.release
        log["version"] = uname.version
        log["machine"] = uname.machine
        log["processor"] = uname.processor
        log["1"] = "---"
        log["boot time"] = f"{bt.day}.{bt.month}.{bt.year} {bt.hour}:{bt.minute}:{bt.second}"
        log["2"] = "---"
        log["CPU Info"] = ""
        log["actual cores"] = psutil.cpu_count(logical=False)
        log["logical cores"] = psutil.cpu_count(logical=True)
        log["max frequency"] = f"{psutil.cpu_freq().max:.1f}Mhz"
        log["current frequency"] = f"{psutil.cpu_freq().current:.1f}Mhz"
        log["CPU Usage"] = f"{psutil.cpu_percent()}%"
        log["CPU Usage/Core"] = "\n".join(_1)
        log["3"] = "---"
        log["RAM Info"] = ""
        log["total"] = f"{adjust_size(virtual_mem.total)}"
        log["available"] = f"{adjust_size(virtual_mem.available)}"
        log["used"] = f"{adjust_size(virtual_mem.used)}"
        log["percentage"] = f"{virtual_mem.percent}%"
        log["4"] = "---"
        log["SWAP"] = ""
        log["total"] = f"{adjust_size(swap.total)}"
        log["free"] = f"{adjust_size(swap.free)}"
        log["used"] = f"{adjust_size(swap.used)}"
        log["percentage"] = f"{swap.percent}%"

        with open("_.log", "w") as fp:
            fp.write("\n".join([f"{key.title()}: {log[key]}" if log[key] != "---" else "\n" for key in log]))

        await message.author.send(file=discord.File(fp="_.log", filename=f"LOGS {datetime.now()}.log"))
