import asyncio
import os
import threading
from dotenv import load_dotenv
from ensembledata.api import EDClient
from functions import new_channel
from moderation import *

load_dotenv()
api_token = str(os.getenv('API_TOKEN'))
api = EDClient(token=api_token)

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
    @app_commands.checks.has_permissions(manage_guild=True)
    async def link_tiktok(interaction: discord.Interaction, username: str):
        file_path = f'{interaction.guild}.txt'
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if 'tiktok:' in line:
                lines[i] = f'tiktok:{username}\n'
        if not any('tiktok:' in line for line in lines):
            lines.append(f'tiktok:{username}\n')
        with open(file_path, 'w') as file:
            file.writelines(lines)
        await interaction.response.send_message(f"The TikTok account for {username} is now linked")

    @bot.command(name="notify_tiktok_posts", description="notify the channel whenever the linked user posts")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def notify_tiktok_posts(interaction: discord.interactions):#check if username is linked
        await interaction.response.defer()
        channel = discord.utils.get(interaction.guild.channels, name="posts")
        last_post_url="None"
        with open(f"{channel.guild}.txt", "r") as file:
            for line in file:
                if "tiktok" in line:
                    line = line.strip()
                    username = line[7:]
                    break
        if not any('tiktok:' in line for line in lines):
            await interaction.followup.send("there is no username linked")
            return
        async def post_tiktok_url():
            nonlocal last_post_url
            while not stop_event_tiktok.is_set():
                result = api.tiktok.user_posts_from_username(
                    username=username,
                    depth=1,
                )
                if result.data["data"]:
                    new_post_url = result.data["data"][0]["share_url"]
                else:
                    new_post_url = "None"
                    await interaction.followup.send(f"No posts found for {username}.")
                    await interaction.followup.send(f"this could be due to entering your username wrong. check it using /check linked tiktok account")

                if last_post_url != new_post_url:
                    await channel.send(new_post_url)
                    last_post_url = new_post_url
            await asyncio.sleep(300)
        stop_event_tiktok.clear()
        asyncio.create_task(post_tiktok_url())
        await interaction.followup.send(f"Whenever {username} posts you will not be notified")

    @bot.command(name="stop_tiktok_posts", description="stop notifying the channel when linked user posts")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def stop_tiktok_posts(interaction: discord.interactions):
        stop_event_tiktok.set()
        await interaction.response.send_message("The server will not be notified when a new TikTok post is made")

    @bot.command(name="check_linked_tiktok_account", description="check which tiktok account is linked to the server")
    async def check_linked_tiktok_account(interaction: discord.interactions):
        file_path = f'{interaction.guild}.txt'
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if 'tiktok:' in line:
                username = line[7:]
                await interaction.response.send_message(f"the linked tiktok account is for @{username}")
        if not any('tiktok:' in line for line in lines):
            await interaction.response.send_message("there is no tiktok account linked")

    @bot.command(name="link_instagram", description="link your instagram account to the server to notify people about posts")
    @app_commands.describe(username="what is you username")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def link_instagram(interaction: discord.Interaction, username: str):
        await interaction.response.defer()
        file_path = f'{interaction.guild}.txt'
        result = api.instagram.user_detailed_info(
            username=username,
        )
        id = result.data["id"]
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if 'instagram:' in line:
                lines[i] = f'instagram:{id}\n'
                lines[i+1] = f'insta_username:{username}\n'
        if not any('instagram:' in line for line in lines):
            lines.append(f'instagram:{id}\n')
            lines.append(f'insta_username:{username}\n')
        with open(file_path, 'w') as file:
            file.writelines(lines)
        await interaction.followup.send(f"The Instagram account for {username} is now linked")

    @bot.command(name="notify_instagram_reels", description="notify the channel whenever the linked user posts")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def notify_instagram_reels(interaction: discord.interactions):
        await interaction.response.defer()
        channel = discord.utils.get(interaction.guild.channels, name="posts")
        last_reels_url = ""
        with open(f"{channel.guild}.txt", "r") as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if "instagram" in line:
                line = line.strip()
                id = int(line[10:])
                break
        if not any('instagram:' in line for line in lines):
            await interaction.followup.send("there is no username linked")
            return
        async def post_instagram_url():
            nonlocal last_reels_url
            while not stop_event_instagram.is_set():
                result = api.instagram.user_reels(
                    user_id=id,
                    depth=1,
                    chunk_size=3,
                )
                username = result.data["reels"][0]["media"]["user"]["username"]
                if result.data["reels"]:
                    reel_id = result.data["reels"][0]["media"]["code"]
                    new_reels_url = f"https://www.instagram.com/reel/{reel_id}/"
                else:
                    new_reels_url = "None"
                    await interaction.followup.send(f"No posts found for {username}.")
                    await interaction.followup.send(
                        f"this could be due to entering your username wrong. check it using /check linked instagram account")

                if last_reels_url != new_reels_url:
                    await channel.send(new_reels_url)
                    last_reels_url = new_reels_url
            await asyncio.sleep(300)
        stop_event_instagram.clear()
        asyncio.create_task(post_instagram_url())
        await interaction.followup.send(f"Whenever you post a reel the server will be notified")

    @bot.command(name="stop_instagram_reels", description="stop notifying the channel when linked user posts")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def stop_instagram_posts(interaction: discord.interactions):
        stop_event_instagram.set()
        await interaction.response.send_message("The server will not be notified when a new instagram post is made")

    @bot.command(name="check_linked_instagram_account", description="check which instagram account is linked to the server")
    async def check_linked_instagram_account(interaction: discord.interactions):
        file_path = f'{interaction.guild}.txt'
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if 'insta_username:' in line:
                username = line[15:]
                await interaction.response.send_message(f"the linked instagram account is for @{username}")
        if not any('insta_username:' in line for line in lines):
            await interaction.response.send_message("there is no instagram account linked")

    @bot.command(name="link_youtube", description="link your youtube account to the server to notify people about posts")
    @app_commands.describe(username="what is your channel name")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def link_youtube(interaction: discord.Interaction, username: str):
        file_path = f'{interaction.guild}.txt'
        result = api.youtube.channel_username_to_id(
            username=username,
        )
        id = result.data
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if 'youtube:' in line:
                lines[i] = f'youtube:{id}\n'
                lines[i+1] = f'youtub_username:{username}\n'
        if not any('youtube:' in line for line in lines):
            lines.append(f'youtube:{id}\n')
            lines.append(f'youtub_username:{username}\n')
        with open(file_path, 'w') as file:
            file.writelines(lines)
        await interaction.response.send_message(f"The Youtube account for {username} is now linked")

    @bot.command(name="notify_youtube_posts", description="notify the channel whenever the linked user posts")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def notify_youtube_posts(interaction: discord.interactions):
        await interaction.response.defer()
        channel = discord.utils.get(interaction.guild.channels, name="posts")
        last_video_url = ""
        last_short_url = ""
        with open(f"{channel.guild}.txt", "r") as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if "youtube" in line:
                line = line.strip()
                id = line[8:]
                break
        if not any('youtube:' in line for line in lines):
            await interaction.followup.send("there is no username linked")
            return

        async def post_youtube_url():
            global new_short_url, new_video_url
            nonlocal last_video_url, last_short_url
            while not stop_event_youtube.is_set():
                video_result = api.youtube.channel_videos(
                    channel_id=id,
                    depth=1,
                )
                shorts_result = api.youtube.channel_shorts(
                    channel_id=id,
                    depth=1,
                )
                username = video_result.data["user"]["title"]
                if video_result.data["videos"]:
                    video_id = video_result.data["videos"][0]["richItemRenderer"]["content"]["videoRenderer"]["videoId"]
                    new_video_url = f"https://www.youtube.com/watch?v={video_id}"
                if shorts_result.data["shorts"]:
                    shorts_id = shorts_result.data["shorts"][0]["richItemRenderer"]["content"]["reelItemRenderer"]["onTap"]["innertubeCommand"]["commandMetadata"]["webCommandMetadata"]["url"]
                    new_short_url = f"https://www.youtube.com/shorts/{shorts_id}"
                else:
                    new_video_url = "None"
                    await interaction.followup.send(f"No posts found for {username}.")
                    await interaction.followup.send(
                        f"this could be due to entering your username wrong. check it using /check linked youtube account")

                if last_video_url != new_video_url:
                    await channel.send(new_video_url)
                    last_video_url = new_video_url
                if last_short_url != new_short_url:
                    await channel.send(new_short_url)
                    last_short_url = new_short_url
            await asyncio.sleep(300)

        stop_event_youtube.clear()
        asyncio.create_task(post_youtube_url())
        await interaction.followup.send(f"Whenever you post the server will be notified")

    @bot.command(name="stop_youtube_posts", description="stop notifying the channel when linked user posts")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def stop_youtube_posts(interaction: discord.interactions):
        stop_event_youtube.set()
        await interaction.response.send_message("The server will not be notified when a new youtube post is made")

    @bot.command(name="check_linked_youtube_account", description="check which youtube account is linked to the server")
    async def check_linked_youtube_account(interaction: discord.interactions):
        file_path = f'{interaction.guild}.txt'
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for i, line in enumerate(lines):
            if 'youtub_username:' in line:
                username = line[17:]
                await interaction.response.send_message(f"the linked youtube account is for @{username}")
        if not any('youtub_username:' in line for line in lines):
            await interaction.response.send_message("there is no youtube account linked")
