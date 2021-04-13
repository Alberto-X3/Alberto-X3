import discord
import Utils


HELP = Utils.Help("lists all profiles", "shows you the history from all profiles of the Bot and the creator")
EVENTS = [Utils.EVENT.on_message]
ALIASES = ["img", "profile", "profiles"]

_00 = "https://media.discordapp.net/attachments/779620254396579850/831499354270335006/00-Alberto-X3_ft.Albert.png"
_01 = "https://media.discordapp.net/attachments/779620254396579850/831501108731314196/01-Alberto-X3_ft.Dr.Negativ.png"
_02 = "https://media.discordapp.net/attachments/779620254396579850/831501111676239882/02-Alberto-X3_ft.Dr.Negativ.png"


async def __main__(client: discord.Client, _event: int, message: discord.Message):
    try:
        await message.channel.send(embed=discord.Embed(description=f"""
    __History:__
    
    • [__00__]({_00}) by <@546320163276849162>
    • [__01__]({_01}) by <@665288034274639873>
    • [__02__]({_02}) by <@665288034274639873>

    """))

    except Exception as e:
        await Utils.send_exception(client=client, exception=e, source_name=__name__)
