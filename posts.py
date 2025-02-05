import time
import threading
import os
from functions import new_channel
from moderation import *
from ensembledata.api import EDClient
api = str(os.getenv('API_TOKEN'))
stop_event_tiktok = threading.Event()
stop_event_instagram = threading.Event()
stop_event_youtube = threading.Event()


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

    @bot.command(name="notify_tiktok_posts", description="notify the channel whenever the linked user posts")
    async def notify_tiktok_posts(interaction: discord.interactions):
        channel = discord.utils.get(interaction.guild.channels, name="posts")
        last_post_url = ""
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
        stop_event_tiktok.clear()
        timer_thread_tiktok = threading.Thread(target=post_url)
        timer_thread_tiktok.daemon = True
        timer_thread_tiktok.start()
        
        def post_url():
            time.sleep(300)
            if not stop_event_tiktok.is_set():
                if last_post_url != new_post_url:
                    channel.send(new_post_url)
                    last_post_url = new_post_url
        await interaction.response.send(f"Whenever {username} posts you will not be notified")

    @bot.command(name="stop_tiktok_posts", description="stop notifing the channel when linked user posts")
    async def stop_tiktok_posts(interaction: discord.interactions):
        stop_event_tiktok.set()
        await interaction.response.send_message("The server will not be notified when a new TikTok post is made")

    @bot.command(name="link_instagram", description="link your instagram account to the server to notify people about posts")
    @app_commands.describe(username="what is you username")
    async def link_instagram(interaction: discord.Interaction, username: str):
        file_path = f'{interaction.guild}.txt'
        result = api.instagram.user_detailed_info(
            username=username,
        )
        id = result.data["data"]["id"]
        with open(file_path, 'w') as file:
            file.write(f"Instagram:{id} \n")
        await interaction.response.send_message(f"The Instagram account for {username} is now linked")
        await interaction.response.send_message(f"Any new posts will now me announced in this channel")

    @bot.command(name="notify_instagram_posts", description="notify the channel whenever the linked user posts")
    async def notify_instagram_posts(interaction: discord.interactions):
        channel = discord.utils.get(interaction.guild.channels, name="posts")
        last_post_url = ""
        last_reels_url = ""
        with open(f"{channel.guild}.txt", "r") as file:
            for line in file:
                if "instagram" in line:
                    line = line.strip()
                    id = line[9:]
                    break
        result = client.instagram.user_posts(
            user_id=id,
            depth=1,
        )
        new_post_url = result.data["data"][0]["share_url"]
        result = client.instagram.user_reels(
            user_id=18428658,
            depth=1,
        )
        new_reels_url = result.data["data"][0]["share_url"]
        stop_event_instagram.clear()
        timer_thread_instagram = threading.Thread(target=post_url)
        timer_thread_instagram.daemon = True
        timer_thread_instagram.start()
        def post_url():
            time.sleep(300)
            if not stop_event_tiktok.is_set():
                if last_post_url != new_post_url:
                    channel.send(new_post_url)
                    last_post_url = new_post_url
                if last_reels_url != new_reels_url:
                    channel.send(new_reels_url)
                    last_reels_url = new_reels_url
        await interaction.response.send(f"Whenever {username} posts you will not be notified") #TODO get username from reels or posts

    @bot.command(name="stop_instagram_posts", description="stop notifing the channel when linked user posts")
    async def stop_instagram_posts(interaction: discord.interactions):
        stop_event_instagram.set()
        await interaction.response.send_message("The server will not be notified when a new instagram post is made")

    @bot.command(name="link_youtube", description="link your youtube account to the server to notify people about posts")
    @app_commands.describe(username="what is your username")
    async def link_youtube(interaction: discord.Interaction, username: str):
        file_path = f'{interaction.guild}.txt'
        result = client.youtube.channel_username_to_id(
            username=username,
        )
        id = result.data
        with open(file_path, 'w') as file:
            file.write(f"Youtube:{id} \n")
        await interaction.response.send_message(f"The Youtube account for {username} is now linked")

    @bot.command(name="notify_youtube_posts", description="notify the channel whenever the linked user posts")
    async def notify_youtube_posts(interaction: discord.interactions):
        channel = discord.utils.get(interaction.guild.channels, name="posts")
        last_video_url = ""
        last_shorts_url = ""
        with open(f"{channel.guild}.txt", "r") as file:
            for line in file:
                if "youtube" in line:
                    line = line.strip()
                    id = line[7:]
                    break
        result = client.youtube.channel_videos(
            channel_id=id,
            depth=1,
        )
        new_video_url = result.data["data"][0]["share_url"] #TODO check dictionary
        result = client.youtube.channel_shorts(
            channel_id=id,
            depth=1,
        )
        new_shorts_url = result.data["data"][0]["share_url"]
        stop_event_youtube.clear()
        timer_thread_youtube = threading.Thread(target=post_url)
        timer_thread_youtube.daemon = True
        timer_thread_youtube.start()
        def post_url():
            time.sleep(300)
            if not stop_event_tiktok.is_set():
                if last_video_url != new_video_url:
                    channel.send(new_video_url)
                    last_video_url = new_video_url
                if last_shorts_url != new_shorts_url:
                    channel.send(new_shorts_url)
                    last_shorts_url = new_shorts_url
        await interaction.response.send(f"Whenever {username} posts you will not be notified") #TODO get username from reels or posts

    @bot.command(name="stop_youtube_posts", description="stop notifing the channel when linked user posts")
    async def stop_youtube_posts(interaction: discord.interactions):
        stop_event_youtube.set()
        await interaction.response.send_message("The server will not be notified when a new youtube post is made")
    
    @bot.command(name="check_for_new_post", description="checks all linked socials for new posts")
    async def check_for_new_posts(interaction: discord.interactions):
        pass

#TODO use try catch statements to do error checking
#TODO if no username linked print no account linked