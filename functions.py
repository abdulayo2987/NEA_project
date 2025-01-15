import discord

async def new_channel(guild, name):
    guild = guild
    name = name
    existing_channel = discord.utils.get(guild.channels, name)
    if not existing_channel:
        channel = await guild.create_text_channel(name)
        print("channel created")
        return channel.id
    else:
        channel = discord.utils.get(guild.channels, name)
        await channel.delete(reason="cuz i said so")
        print("channel deleted")
        channel = await guild.create_text_channel(name)
        print("channel created")
        return channel.id