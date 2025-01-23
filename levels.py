from functions import new_channel
from moderation import *

async def new_levels_channel(guild):
    await new_channel(guild, "levels")
    channel = discord.utils.get(guild.channels, name="levels")
    await channel.set_permissions(guild.default_role, send_messages=True)

def leveling_commands():
    pass