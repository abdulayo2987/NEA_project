from trie import trie
import discord
from discord import app_commands
from run import Client, Intents
from discord.ext import commands

intents = Intents.default()
tree = app_commands.CommandTree(Client)
Banned_list = trie()

def moderation_commands():

    @tree.command(name = "ban_word")
    @app_commands.describe(banned_word_add = "what word do you want me to ban?")
    async def add_to_banned_words(interaction: discord.Interaction, banned_word_add: str):
        await interaction.response.send_message(f'"{banned_word_add}" has been banned.')

    def delete_from_banned_words(message):
        pass

    def list_all_banned_words():
        pass

    def check_if_in_banned_words(message):
        pass

    def check_user_message(message):
        pass

