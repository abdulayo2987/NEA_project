# imports
import os
import sqlite3
from dotenv import load_dotenv
from discord import Intents, Client, Message

#Get and set token from .env file so it can only be accessed by me
load_dotenv()
TOKEN = str(os.getenv('DISCORD_TOKEN'))

#Gives the Bot permissions so it can read/write messages
intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)

@client.event
async def on_ready():
    print(f'logged in as {client.user}')

def main() -> None:
    client.run(str(TOKEN))

if __name__ == '__main__':
    main()
