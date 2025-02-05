import time
import threading
import os
from functions import new_channel
from moderation import *
from ensembledata.api import EDClient
API_TOKEN = str(os.getenv('API_TOKEN'))

async def new_posts_channel(guild):
    await new_channel(guild, "posts")
    channel = discord.utils.get(guild.channels, name="posts")
    await channel.set_permissions(guild.default_role, send_messages=False)

def posts_commands():
    @bot.command(name="link_tiktok", description="link your tiktok account to the server to notify people about posts")
    @app_commands.describe(username="what is you username")
    async def link_tiktok(interaction: discord.Interaction, username: str):
        file_path = f'{interaction.guild}.txt'
        with open(file_path, 'w') as file:
            file.write(f"tiktok:{username} \n")
        await interaction.response.send_message(f"The TikTok account for {username} is now linked")
        await interaction.response.send_message(f"Any new posts will now me announced in this channel")


    @bot.command(name="link_instagram", description="link your instagram account to the server to notify people about posts")
    @app_commands.describe(username="what is you username")
    async def link_instagram(interaction: discord.Interaction, username: str):
        file_path = f'{interaction.guild}.txt'
        with open(file_path, 'w') as file:
            file.write(f"TikTok:{username} \n")
        await interaction.response.send_message(f"The Instagram account for {username} is now linked")
        await interaction.response.send_message(f"Any new posts will now me announced in this channel")


    @bot.command(name="link_youtube", description="link your youtube account to the server to notify people about posts")
    @app_commands.describe(username="what is your username")
    async def link_youtube(interaction: discord.Interaction, username: str):
        file_path = f'{interaction.guild}.txt'
        with open(file_path, 'w') as file:
            file.write(f"TikTok:{username} \n")
        await interaction.response.send_message(f"The Youtube account for {username} is now linked")
        await interaction.response.send_message(f"Any new posts will now me announced in this channel")

    new_tiktok_post()

def new_tiktok_post():
    channel = discord.utils.get(guild.channels, name="posts")
    last_post_url = ""
    api = EDClient(token=API_TOKEN)
    #TODO get username from text file
    with open(f"{channel.guild}.txt", "r") as file:
        for line in file:
            if "tiktok" in line:
                line = line.strip()
                username = line[7:]
                break
    result = api.tiktok.user_posts_from_username(
        username=username,
        depth=1,
    )
    new_post_url = result.data["data"][0]["share_url"]
    while True:
        time.sleep(300)
        if last_post_url != new_post_url:
            channel.send(new_post_url)
            last_post_url = new_post_url

timer_thread = threading.Thread(target=new_tiktok_post)
timer_thread.daemon = True
timer_thread.start()

