"""
adds automatically a role to a member to have it "clued" on the member
"""
from discord import Member, Role, Client, Guild
from Utils import EVENT, send_exception


EVENTS = [EVENT.on_member_update, EVENT.on_ready]

ROLES = {
    "WARNING: SPOILER!!!": 861238496484130816
}
STICKY = {
    752762890288758784: {  # Nxnx
        "roles": [
            ROLES["WARNING: SPOILER!!!"]
        ]
    }
}


async def __main__(client: Client, _event: int, *member: Member):
    try:
        guild: Guild = client.guilds[0]

        if _event == EVENT.on_member_update:
            if member[0].roles != member[1].roles and member[1].id in STICKY:
                await member[1].add_roles(
                    *[guild.get_role(r) for r in STICKY[member[1].id]["roles"]]
                )

        elif _event == EVENT.on_ready:
            for m in STICKY:
                m = guild.get_member(m)
                await m.add_roles(
                    *[guild.get_role(r) for r in STICKY[m.id]["roles"]]
                )

    except Exception as e:
        await send_exception(client=client, exception=e, source_name=__name__)
