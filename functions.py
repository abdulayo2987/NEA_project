import discord

async def new_channel(guild, name):
    existing_channel = discord.utils.get(guild.channels, name=name)
    if not existing_channel:
        channel = await guild.create_text_channel(name)
        return channel
    else:
        channel = discord.utils.get(guild.channels, name=name)
        await channel.delete(reason="cuz i said so")
        channel = await guild.create_text_channel(name)
        return channel

