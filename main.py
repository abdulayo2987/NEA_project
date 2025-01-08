# Imports
import os
import discord
import sqlite3
from discord import Message
from dotenv import load_dotenv
from moderation import moderation_commands, check_message, client, bot, banned_words
#fix no module named 'audioop' by deleting import from python file

# Load environment variables
load_dotenv()
TOKEN = str(os.getenv('DISCORD_TOKEN'))



moderation_commands()
check_message()

# Event listener
@client.event
async def on_ready():
    if not os.path.exists("has_run.txt"):
        async def get_user_ids():
            with open("has_run.txt", "w") as f:
                f.write("This program has run once.")
            print("is running now?")
            file = "NEA.sqlite"
            connection = sqlite3.connect(file)
            cursor = connection.cursor()
            members = await client.fetch_members().flatten()
            for member in members:
                cursor.execute("""
                INSERT INTO users (user_id, username, join_date, level) 
                VALUES (?, ?, ?, ?)
                """, (member.id, member.global_name, member.joined_at, 0))

            connection.commit()
            connection.close()

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
