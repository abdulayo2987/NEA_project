from discord import app_commands, Client, Intents
import discord
from trie import trie

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)
tree = app_commands.CommandTree(client)

banned_words = trie()
banned_words_punishments = {
    "test" : "nothing"
}


def moderation_commands():

    @tree.command(name="ban_word")
    @app_commands.describe(banned_word_add="What word do you want to ban?", banned_words_punishment="What punishment do you want for someone that uses this word")
    async def ban_word(interaction: discord.Interaction, banned_word_add: str):
        banned_words.insert(banned_word_add)
        await interaction.response.send_message(f'"{banned_word_add}" has been banned.')

    @tree.command(name="unban_word")
    @app_commands.describe(unbanned_word_add="What word do you want to unban?")
    async def unban_word(interaction: discord.Interaction, unbanned_word_add: str):
        banned_words.delete(unbanned_word_add)
        await interaction.response.send_message(f'"{unbanned_word_add}" has been unbanned.')

    @tree.command(name="list_banned_words")
    async def list_all_banned_words(interaction: discord.Interaction):
        await interaction.response.send_message(banned_words.list_words())

    @tree.command(name="check_banned_words")
    @app_commands.describe(message="What word do you me to check for?")
    async def check_if_in_banned_words(interaction: discord.Interaction, check_word: str):
        if banned_words.search(check_word) == True:
            print(f'"{check_word}" is banned.')
        else:
            print(f'"{check_word}" is not banned.')

    def check_user_message(message):
        pass

