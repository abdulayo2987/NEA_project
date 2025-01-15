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
check_message()
new_member_join()
first_message_sent = False

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
    global first_message_sent
    guild = message.guild
    if not first_message_sent:
        first_message_sent = True
        if os.path.exists(f'{guild}.txt'):
            return
        else:
            file_path = f'{guild}.txt'
            await new_roles_channel(guild)
            await new_welcome_channel(guild)
            with open(file_path, 'w') as file:
                file.write("welcome and role channel created \n")
            fill_moderation()
            fill_users()
            fill_guilds(guild)
            with open(file_path, 'w') as file:
                file.write("database filled\n")


# Main function
def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()
