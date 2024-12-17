# Imports
import os
import discord
from dotenv import load_dotenv
from moderation import moderation_commands, client, tree

# Load environment variables
load_dotenv()
TOKEN = str(os.getenv('DISCORD_TOKEN'))

moderation_commands()

# Event listeners
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    try:
        synced = await tree.sync()
        print(f'Commands synced successfully: {len(synced)} command(s)')
    except discord.Forbidden as e:
        print(f"Failed to sync commands: {e}")
    print([command.name for command in synced])


# Main function
def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()
