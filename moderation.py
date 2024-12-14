from discord import app_commands, Client, Intents
import discord

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)
tree = app_commands.CommandTree(client)


def moderation_commands():

    @tree.command(name="ban_word")
    @app_commands.describe(banned_word_add="What word do you want to ban?")
    async def ban_word(interaction: discord.Interaction, banned_word_add: str):
        await interaction.response.send_message(f'"{banned_word_add}" has been banned.')

    def delete_from_banned_words(message):
        pass

    def list_all_banned_words():
        pass

    def check_if_in_banned_words(message):
        pass

    def check_user_message(message):
        pass

