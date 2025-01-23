#store username in text file 
#use apis to find latest posts
#notify anyone that wants to know 
from functions import new_channel
from moderation import *

async def new_posts_channel(guild):
    await new_channel(guild, "postss")
    channel = discord.utils.get(guild.channels, name="posts")
    await channel.set_permissions(guild.default_role, send_messages=True)

@bot.command(name="link_TikTok", description="link your tiktok account to the server to notify people about posts")
@app_commands.describe(username="what is you username")
async def link_TikTok(interaction: discord.Interaction, username: str):
    pass

@bot.command(name="link_instagram", description="link your instagram account to the server to notify people about posts")
@app_commands.describe(username="what is you username")
async def link_instagram(interaction: discord.Interaction, username: str):
    pass

@bot.command(name="link_youtube", description="link your youtube account to the server to notify people about posts")
@app_commands.describe(username="what is you username")
async def link_youtube(interaction: discord.Interaction, username: str):
    pass
