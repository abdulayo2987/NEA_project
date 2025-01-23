# Imports
import os
from dotenv import load_dotenv
from datbase import *
from welcome import *
from roles import *
#fix no module named 'audioop' by deleting import from python file

# Load environment variables
load_dotenv()
TOKEN = str(os.getenv('DISCORD_TOKEN'))

moderation_commands()
role_commands()
check_message()
new_member_join()

@client.event
async def on_ready():
    try:
        synced = await bot.sync()
        print(f'Commands synced successfully: {len(synced)} command(s)')
    except discord.Forbidden as e:
        print(f"Failed to sync commands: {e}")

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    guild = message.guild
    file_path = f'{guild}.txt'
    try:
        with open(file_path, "r") as file:
            first_message = file.readline().strip()
        if first_message == "first message has been sent":
            return
    except FileNotFoundError:
        #make new caregory called important and add thes channels to it
        await new_roles_channel(guild)
        await new_welcome_channel(guild)
        with open(file_path, 'w') as file:
            file.write("welcome and role channel created \n")
        fill_database(guild)
        with open(file_path, 'w') as file:
            file.write("database filled\n")


# Main function
def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()
