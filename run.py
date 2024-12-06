# imports
import os
import discord
from dotenv import load_dotenv

def run_bot():
    #Get and set token from .env file so it can only be accessed by me
    load_dotenv()
    TOKEN = str(os.getenv('DISCORD_TOKEN'))
    #Gives the Bot permissions so it can read/write messages
    intents = Intents.default()
    intents.message_content = True # NOQA
    client = Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')
        try:
            await tree.sync()
        except Exception as e:
            print(e)

    client.run(token=str(TOKEN))


#https://youtu.be/emHIBz3r4jI