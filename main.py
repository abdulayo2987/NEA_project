# Imports
import os
import discord
import sqlite3
from discord import Message
from dotenv import load_dotenv
from moderation import moderation_commands, check_message, client, bot, banned_words

# Load environment variables
load_dotenv()
TOKEN = str(os.getenv('DISCORD_TOKEN'))

moderation_commands()
check_message()

# Event listener
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    try:
        synced = await bot.sync()
        print(f'Commands synced successfully: {len(synced)} command(s)')
    except discord.Forbidden as e:
        print(f"Failed to sync commands: {e}")


# Main function
def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()
