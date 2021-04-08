import discord
import Utils
from random import randrange


EVENTS = [Utils.EVENT.on_voice_state_update]
name_range = [1, 1793]


async def __main__(client: discord.Client, _event: int, member: discord.Member,
                   before: discord.VoiceState, after: discord.VoiceState):
    try:
        if before.channel is not None:
            if before.channel.name.startswith("Talk "):
                for name in range(*name_range):
                    if before.channel.name == f"Talk {name}":
                        if len(before.channel.members) == 0:
                            await before.channel.delete()
                        break

        if after.channel is not None:
            if after.channel.id == 829778748026257458:
                name = randrange(*name_range)
                new_talk: discord.VoiceChannel = await after.channel.clone(
                    name=f"Talk {name}")

                await member.move_to(new_talk)

    except Exception as e:
        await Utils.send_exception(client=client, exception=e, source_name=__name__)
