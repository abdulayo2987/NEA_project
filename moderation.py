from trie import trie
import discord

tree = app_commands.CommandTree(client)

@tree.command(name = "ban word")
@app_commands.describe(banned_word_add = "what word do you want me to ban?")
async def add_to_banned_words(interaction: discord.Interaction, banned_word_add: str):
    pass

def delete_from_banned_words(message):
    pass

def list_all_banned_words():
    pass

def check_if_in_banned_words(message):
    pass

def check_user_message(message):
    pass