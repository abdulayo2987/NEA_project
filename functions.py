import discord
import hashlib
import os


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

def custom_hash(data: str, salt: bytes) -> str:
    hashed_value = int.from_bytes(salt, "big")
    for char in data:
        hashed_value ^= ord(char)  # XOR each character's ASCII value
        hashed_value = (hashed_value << 8 | hashed_value >>  2) & 0xFFFFFFFF  #
    return hashlib.sha256(str(hashed_value).encode()).hexdigest()


