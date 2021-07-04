"""
adds automatically a role to a member to have it "clued" on the member
"""
from discord import Member, Client, Guild
from Utils import EVENT, send_exception


EVENTS = [EVENT.on_member_update, EVENT.on_ready]

ROLES = {
    "WARNING: SPOILER!!!": 861238496484130816,
    "WARNING: NO PERMS FOR THIS PERSON!!!": 861327480554782751
}
STICKY = {
    752762890288758784: {  # Nxnx
        "roles": [
            ROLES["WARNING: SPOILER!!!"]
        ]
    },
    644068957627744266: {  # Ingo2004
        "roles": [
            ROLES["WARNING: NO PERMS FOR THIS PERSON!!!"]
        ]
    }
}


async def __main__(client: Client, _event: int, *member: Member):
    try:
        guild: Guild = client.guilds[0]

        if _event == EVENT.on_member_update:
            if member[0].roles != member[1].roles and member[1].id in STICKY:
                gr = guild.get_role
                await member[1].add_roles(
                    *[gr(r) for r in STICKY[member[1].id]["roles"]
                      if gr(r) is not None]
                )

        elif _event == EVENT.on_ready:
            gr = guild.get_role
            for m in STICKY:
                m = guild.get_member(m)
                await m.add_roles(
                    *[gr(r) for r in STICKY[m.id]["roles"]
                      if gr(r) is not None]
                )

    except Exception as e:
        await send_exception(client=client, exception=e, source_name=__name__)
