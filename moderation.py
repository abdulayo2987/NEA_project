import sqlite3
import discord
from datetime import timedelta, datetime
from typing import Literal
from trie import trie
from discord import app_commands, Client, Intents, Message


intents = Intents.default()
intents.message_content = True
intents.reactions = False
intents.voice_states = True
intents.members = True
intents.guilds = True
client = Client(intents=intents)
bot = app_commands.CommandTree(client)

file = "nea.sqlite"

banned_words = trie()
punishments_list = {
    1 : "warn",
    2 : "mute",
    3 : "kick",
    4 : "ban"
}

banned_words_punishments = {
    "fool":"warn"
}

def moderation_commands():

    @bot.command(name="sync", description="sync commands")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def sync(interaction: discord.Interaction):
        await bot.sync()
        await interaction.response.send_message("Commands synced!")

    @bot.command(name="ban_word", description="Ban a word from being used in the server.")
    @app_commands.describe(banned_word_add="What word do you want to ban?", punishment="What punishment do you want to give for using this word?")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def ban_word(interaction: discord.Interaction, banned_word_add: str, punishment: Literal["warn", "mute", "kick", "ban"]):
        banned_words.insert(banned_word_add)
        banned_words_punishments[banned_word_add] = punishment
        await interaction.response.send_message(f'"{banned_word_add}" has been banned.')

    @bot.command(name="unban_word", description="Unban a word from being used in the server.")
    @app_commands.describe(unbanned_word="What word do you want to unban?")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def unban_word(interaction: discord.Interaction, unbanned_word: str):
        banned_words.delete(unbanned_word)
        if unbanned_word in banned_words_punishments:
            del banned_words_punishments[unbanned_word]
        await interaction.response.send_message(f'"{unbanned_word}" has been unbanned.')

    @bot.command(name="list_banned_words", description="List all banned words in the server.")
    async def list_all_banned_words(interaction: discord.Interaction):
        await interaction.response.send_message(banned_words.list_words())

    @bot.command(name="mute")
    @app.command.describe(user="who do you want to mute", reason="why do you want to mute this user" time="how long do you want to time them out for(mins)")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def mute(interaction: discord.Interaction, user: discord.Member, reason: str, time: int):
        await interaction.response.send_message(f"<@{user.id}> you have been muted for 15 minutes for {reason} ")
        await interaction.Member.edit(timeout=discord.utils.utcnow() + timedelta(seconds=time*60))
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute(f"""
        INSERT INTO moderation_actions (user_id, moderator_id, guild_id, action_type, timestamp, reason) 
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user.id, interaction.user.id. interaction.guild.id, "mute", datetime.utcnow(), reason))
        connection.commit()
        connection.close()


    @bot.command(name="kick")
    @app.command.describe(user="who do you want to kick", reason="why do you want to kick them")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def kick(interaction: discord.Interaction, user: discord.Member, reason: str):
        await interaction.guild.kick(user, reason=reason)
        await interaction.response.send_message(f"<@{user.id}> has been kicked for {reason}")
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute(f"""
        INSERT INTO moderation_actions (user_id, moderator_id, guild_id, action_type, timestamp, reason) 
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user.id, interaction.user.id. interaction.guild.id, "kick", datetime.utcnow(), reason))
        connection.commit()
        connection.close()


    @bot.command(name="ban")
    @app.command.describe(user="who do you want to ban", reason="why do you want to ban them")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def ban(interaction: discord.Interaction, user: discord.Member, reason: str):
        await interaction.guild.ban(user, reason=reason)
        await interaction.response.send_message(f"<@{user.id}> has been banned for {reason}")
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute(f"""
        INSERT INTO moderation_actions (user_id, moderator_id, guild_id, action_type, timestamp, reason) 
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user.id, interaction.user.id. interaction.guild.id, "ban", datetime.utcnow(), reason))
        connection.commit()
        connection.close()

    @bot.command(name="check_banned_word", description="Check if a word is banned in the server.")
    @app_commands.describe(check_word="What word do you me to check for?")
    async def check_if_in_banned_words(interaction: discord.Interaction, check_word: str):
        if banned_words.search(check_word):
            await interaction.response.send_message(f'"{check_word}" is banned.')
        else:
            await interaction.response.send_message(f'"{check_word}" is not banned.')
    check_message()

def check_message():
    @client.event
    async def on_message(message: Message):
        words = message.content.split()
        for word in words:
            bad_word = banned_words.search(word)
            if bad_word:
                await moderator_action(message, banned_words_punishments[word], word)
                await message.delete()
                await message.channel.send(f"{client.user.mention} has {banned_words_punishments[word]}ed {message.author.mention} reason: message contained word that is banned")
                break

async def moderator_action(message: Message, punishment: str, bad_word: str):
    if punishment == "warn":
        punishment_level = 1
    elif punishment == "mute":
        punishment_level = 2
    elif punishment == "kick":
        punishment_level = 3
    else:
        punishment_level = 4

    connection = sqlite3.connect(file)
    cursor = connection.cursor()

    cursor.execute(f"""
        SELECT {punishment}_count 
        FROM moderation_stats 
        WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}
        """)
    result = cursor.fetchone()
    if int(result[0]) % 2 == 0 and int(result[0]) != 0:
        punishment = punishments_list[punishment_level+1]


    cursor.execute(f"""
    UPDATE moderation_stats 
    SET {punishment}_count = {punishment}_count + 1 
    WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}
    """)

    cursor.execute(f"""
    INSERT INTO moderation_actions (user_id, moderator_id, guild_id, action_type, timestamp, reason) VALUES
    ({message.author.id},{client.user.id},{message.guild.id},'{punishment}',{message.created_at.date()}, ?)
    """, f"using the word {bad_word}")

    connection.commit()
    connection.close()

    if punishment_level == 1:
        await message.channel.send(f"{client.user.mention} you cannot say '{bad_word}' as it is banned in this server")
    elif punishment_level == 2:
        await message.channel.send(f"{client.user.mention} you have been muted for 15 minutes for saying {bad_word} as it is banned in this server")
        await discord.Member.edit(timeout=discord.utils.utcnow() + timedelta(seconds=900))
    elif punishment_level == 3:
        await message.channel.send(f"{client.user.mention} has been kicked")
        await discord.Member.kick(reason="using banned words")
    elif punishment_level == 4:
        await message.channel.send(f"{client.user.mention} has been banned")
        await discord.Member.ban(reason="using banned words")

    return punishment
