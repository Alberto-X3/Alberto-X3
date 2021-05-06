from discord import Client, Member, Role
from Utils import Help, EVENT, send_exception


HELP = Help(vanish=True, order_1793=True)
EVENTS = [EVENT.on_member_update, EVENT.on_ready]


sep = " | "
nicks = {
    733966411663278141: "Mod",
    828370010866843668: "Sup",
    674637758869930007: "VIP"
}


async def __main__(client: Client, _event: int,
                   before: Member = None, after: Member = None):
    try:
        if _event == EVENT.on_ready:
            for member in client.get_guild(632526390113337346).members:
                await repair(member)
        else:
            await repair(after)

    except Exception as e:
        await send_exception(client=client, exception=e, source_name=__name__)


async def repair(member: Member) -> None:
    if member.top_role in nicks:
        prefix = nicks[member.top_role]
        if member.nick is None or not member.nick.startswith(prefix+sep):
            nick = prefix+sep+member.display_name
            if len(nick) > 32:
                nick = nick[:32]
            await member.edit(nick=nick)
