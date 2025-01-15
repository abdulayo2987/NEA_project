import discord
from functions import new_channel

async def new_welcome_channel(guild):
    channel = new_channel(guild, "welcome")