# Imports
import os
import discord
from dotenv import load_dotenv
from moderation import moderation_commands, client, tree

# Load environment variables
load_dotenv()
TOKEN = str(os.getenv('DISCORD_TOKEN'))

moderation_commands()

# Event listener
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    try:
        synced = await tree.sync()
        print(f'Commands synced successfully: {len(synced)} command(s)')
    except discord.Forbidden as e:
        print(f"Failed to sync commands: {e}")

@client.event
async def on_message(message: Message):
    words = message.content.split()
    for word in words:
        bad = banned_words.search(word)
        if bad == True
            



# Main function
def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()
