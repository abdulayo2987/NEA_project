import math

from discord import app_commands, Client, Intents, Message
import discord
from trie import trie
from typing import Literal
import sqlite3

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)
bot = app_commands.CommandTree(client)

banned_words = trie()
punishments_list = {
    1 : "warn",
    2 : "mute",
    3 : "kick",
    4 : "ban"
}

banned_words_punishments = {
    "porn" : "warn",
}

def moderation_commands():

    @bot.command(name="ban_word", description="Ban a word from being used in the server.")
    @app_commands.describe(banned_word_add="What word do you want to ban?", punishment="What punishment do you want to give for using this word?")
    async def ban_word(interaction: discord.Interaction, banned_word_add: str, punishment: Literal["warn", "mute", "kick", "ban"]):
        banned_words.insert(banned_word_add)
        banned_words_punishments[banned_word_add] = punishment
        await interaction.response.send_message(f'"{banned_word_add}" has been banned.')

    @bot.command(name="unban_word", description="Unban a word from being used in the server.")
    @app_commands.describe(unbanned_word_add="What word do you want to unban?")
    async def unban_word(interaction: discord.Interaction, unbanned_word_add: str):
        banned_words.delete(unbanned_word_add)
        await interaction.response.send_message(f'"{unbanned_word_add}" has been unbanned.')

    @bot.command(name="list_banned_words", description="List all banned words in the server.")
    async def list_all_banned_words(interaction: discord.Interaction):
        await interaction.response.send_message(banned_words.list_words())

    @bot.command(name="check_banned_word", description="Check if a word is banned in the server.")
    @app_commands.describe(check_word="What word do you me to check for?")
    async def check_if_in_banned_words(interaction: discord.Interaction, check_word: str):
        if banned_words.search(check_word):
            await interaction.response.send_message(f'"{check_word}" is banned.')
        else:
            await interaction.response.send_message(f'"{check_word}" is not banned.')

def check_message():
    @client.event
    async def on_message(message: Message):
        words = message.content.split()
        for word in words:
            bad_word = banned_words.search(word)
            if bad_word:
                moderator_action(message, banned_words_punishments[bad_word])
                await message.delete()
                await message.channel.send(f"@{client} has been sanctioned @{message.author}: reason message that is banned: {bad_word}")
                break

def moderator_action(message: Message, punishment: str):
    if punishment == "warn":
        punishment_level = 1
    elif punishment == "mute":
        punishment_level = 2
    elif punishment == "kick":
        punishment_level = 3

    file = "NEA.sqlite"
    connection = sqlite3.connect(file)
    cursor = connection.cursor()

    cursor.execute(f"""
        SELECT {punishment}_count 
        FROM moderation_stats 
        WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}
        """)
    result = cursor.fetchone()
    if math.fmod(result, 2) == 0 and result != 0:
        punishment = banned_words_punishments[punishment_level+1]


    cursor.execute(f"""
    INSERT INTO moderation_stats (user_id, role_id, guild_id) VALUES
    ({message.author.id},{message.author.top_role.id},{message.guild.id})
    ON CONFLICT (user_id, guild_id) DO UPDATE SET {punishment}_count = {punishment}_count + 1
    """)

    cursor.execute(f"""
    INSERT INTO moderation_actions (user_id, moderator_id, guild_id, action_type, timestamp) VALUES
    ({message.author.id},{client.user.id},{message.guild.id},'{punishment}',{message.created_at})
    """)

    connection.commit()
    connection.close()
