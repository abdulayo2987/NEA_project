# imports
import os
import discord
from discord import Client, Intents, app_commands
from dotenv import load_dotenv
from temp import commands, client, tree


load_dotenv()
TOKEN = str(os.getenv('DISCORD_TOKEN'))

@client.event
async def import_commands():
    await  commands()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    try:
        # Attempt to sync the commands
        synced = await tree.sync()
        print(f'Commands synced successfully: {len(synced)} command(s)')
    except discord.Forbidden as e:
        print(f"Failed to sync commands: {e}")

def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()