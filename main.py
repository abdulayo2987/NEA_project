# Imports
import os
import discord
from discord import Message
from dotenv import load_dotenv
from datbase import fill_moderation, fill_guilds, fill_users
from moderation import moderation_commands, check_message, client, bot
from welcome import new_welcome_channel
from roles import new_roles_channel
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


@client.event
async def on_first_message(message: Message) -> None:
    guild = message.guild
    if os.path.exists(f'{guild}.txt'):
        print("first message sent")
    else:
        file_path = f'{guild}.txt'
        new_roles_channel(guild)
        new_welcome_channel()
        with open(file_path, 'w') as file:
            file.write("welcome and role channel created \n")
        fill_moderation()
        fill_users()
        fill_guilds(guild)
        with open(file_path, 'w') as file:
            file.write("database filled\n")
    
    
    print("done")
    if message.author == client.user:
        return
    await message.channel.send("hello")



# Main function
def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()
