from discord import Client, Member
from Utils import Help, EVENT, send_exception


HELP = Help(vanish=True, order_1793=True)
EVENTS = [EVENT.on_member_update, EVENT.on_ready]


sep = " | "
DEV = "Dev"
MOD = "Mod"
SUP = "Sup"
VIP = "VIP"
ALB = "Aty"
nicks = {
    832244630582067270: DEV,  # @Developer
    733966411663278141: MOD,  # @Moderaty
    828370010866843668: SUP,  # @Supporty
    674637758869930007: VIP,  # @VIP

    831629269414182943: ALB,  # @Level 30
    831628612171071498: ALB,  # @Level 25
    831628364803997757: ALB,  # @Level 20
    831628201406627871: ALB,  # @Level 15
    831628459222237227: ALB,  # @Level 10
    831915216475914273: ALB,  # @Level 5

    707911694277673081: ALB,  # @50er
    638630227966296074: ALB,  # @Albertany
}


async def __main__(client: Client, _event: int,
                   before: Member = None, after: Member = None):
    try:
        if _event == EVENT.on_ready:
            for member in client.get_guild(632526390113337346).members:
                await repair(member)
        if _event == EVENT.on_member_update:
            await repair(after)

    except Exception as e:
        await send_exception(client=client, exception=e, source_name=__name__)


async def repair(member: Member) -> None:
    if member.top_role.id in nicks:
        prefix = nicks[member.top_role.id]
        if member.nick is None or not member.nick.startswith(prefix+sep):
            nick = prefix+sep+member.display_name
            if len(nick) > 32:
                nick = nick[:32]
            await member.edit(nick=nick)
