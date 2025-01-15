# Imports
import os
import discord
from discord import Message
from dotenv import load_dotenv
from datbase import fill_database, fill_moderation
from moderation import moderation_commands, check_message, client, bot
#fix no module named 'audioop' by deleting import from python file

# Load environment variables
load_dotenv()
TOKEN = str(os.getenv('DISCORD_TOKEN'))

moderation_commands()
check_message()

# Event listener
@client.event
async def on_ready():
    try:
        synced = await bot.sync()
        print(f'Commands synced successfully: {len(synced)} command(s)')
    except discord.Forbidden as e:
        print(f"Failed to sync commands: {e}")

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('message empty')
        return
    if message.author == client.user:
        return
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
    try:
        response = "hello"
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


@client.event
async def on_message(message: Message) -> None:
    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)
    print(f'[{channel}] {username}: "{user_message}"')
    fill_moderation()
    print("done")
    if message.author == client.user:
        return
    await message.channel.send("fdggd")



# Main function
def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()
