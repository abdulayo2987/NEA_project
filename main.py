# imports
import os
import sqlite3
from dotenv import load_dotenv
from discord import Intents, Client, Message
from moderation import warn_user

#Get and set token from .env file so it can only be accessed by me
load_dotenv()
TOKEN = str(os.getenv('DISCORD_TOKEN'))

#Gives the Bot permissions so it can read/write messages
intents = Intents.default()
intents.message_content = True # NOQA
client = Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('message empty')
        return
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    warn_user(message)
    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)
    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')

def main() -> None:
    client.run(str(TOKEN))

if __name__ == '__main__':
    main()
