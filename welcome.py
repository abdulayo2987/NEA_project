import random
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont
from functions import new_channel
from moderation import *

responses = ["Welcome to our server {guild} {username}! Thanks for joining us!",
             "Hey there! Glad to have you here at our server {guild} {username}, thank you for joining!",
            "Welcome aboard {username}! We're excited to have you with us in {guild}",
            "Thanks for joining {username}! We’re thrilled you’re here at our server {guild}",
            "Welcome to the crew {username}! Let’s have some fun together in our server {guild}!",
            "Hello and welcome {username}! Thanks for being part of our server {guild}.",
            "Welcome {username}! We’re so happy you decided to join us in our server {guild}.",
            "Thank you for joining our server {guild} {username}, make yourself at home!",
            "Yay, you’re here {username}! Welcome to our awesome server {guild}!",
            "A warm welcome to you {username}! Thanks for being here at our server {guild}.",
            "Thanks for hopping in {username}! We’re so glad to have you here at our server {guild}.",
            "Welcome to the party {username}! We’re grateful you could join us in our server {guild}.",
            "So great to see you here {username} welcome to our server {guild}!",
            "Hello, {username}! Thanks for joining our our server {guild}",
            "Welcome {username}! Let’s make some amazing memories together in our server {guild}!",
            ]

async def new_welcome_channel(guild):
    await new_channel(guild, "welcome")
    channel = discord.utils.get(guild.channels, name="welcome")
    await channel.set_permissions(guild.default_role, send_messages=False)
    await channel.send(f"welcome to {guild.name}")

def new_member_join():
    @client.event
    async def on_member_join(member: discord.Member):
        await add_to_database(member)
        await welcome_message(member)
        await welcome_image(member)

async def welcome_message(member):
    channel = discord.utils.get(member.guild.channels, name="welcome")
    message = random.choice(responses)
    message = message.format(username=member.global_name, guild=member.guild.name)
    await channel.send(message)

async def welcome_image(member):
    channel = discord.utils.get(member.guild.channels, name="welcome")
    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    avatar_response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(avatar_response.content)).resize((100, 100))  # Adjust size as needed

    border_size = 3
    scale_factor = 4
    high_res_size = (
        (avatar.size[0] + border_size * 2) * scale_factor,
        (avatar.size[1] + border_size * 2) * scale_factor,
    )
    high_res_canvas = Image.new("RGBA", high_res_size, (0, 0, 0, 0))
    draw_high_res = ImageDraw.Draw(high_res_canvas)

    draw_high_res.ellipse(
        (0, 0, high_res_size[0], high_res_size[1]),
        fill="black",
    )

    avatar_high_res = avatar.resize(
        (avatar.size[0] * scale_factor, avatar.size[1] * scale_factor), Image.Resampling.LANCZOS
    )
    mask = Image.new("L", avatar_high_res.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar_high_res.size[0], avatar_high_res.size[1]), fill=255)

    high_res_canvas.paste(
        avatar_high_res,
        (border_size * scale_factor, border_size * scale_factor),
        mask,
    )

    final_size = (
        avatar.size[0] + border_size * 2,
        avatar.size[1] + border_size * 2,
    )
    final_canvas = high_res_canvas.resize(final_size, Image.Resampling.LANCZOS)

    background = Image.open("background.png")
    background.paste(final_canvas, (200, 80), final_canvas)

    welcome_text = f"{member.name} just joined {member.guild}"
    member_number = f"Member #{member.guild.member_count}"

    draw = ImageDraw.Draw(background)

    font = ImageFont.truetype("arial.ttf", 20)
    bbox = draw.textbbox((0, 0), welcome_text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (background.width - text_width) // 2
    draw.text((x, 200), welcome_text , font=font, fill="black")

    font = ImageFont.truetype("arial.ttf", 15)
    bbox = draw.textbbox((0, 0), member_number, font=font)
    text_width = bbox[2] - bbox[0]
    x = (background.width - text_width) // 2
    draw.text((x, 225),member_number , font=font, fill="black")

    output_path = "welcome.png"
    background.save(output_path)
    await channel.send(file=discord.File(output_path))

async def add_to_database(member):
    file = "nea.sqlite"
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO users (user_id, username, join_date)
    VALUES (?, ?, ?)
    """, (member.id, member.name, member.joined_at))
    cursor.execute("""
    INSERT INTO moderation_stats (user_id, guild_id, top_role_id) 
    VALUES (?, ?, ?)
    """,(member.id, member.guild.id, member.top_role.id))
    cursor.execute("""
    INSERT INTO user_roles ( user_id, guild_id, top_role_id) 
    VALUES (?, ?, ?)
    """, (member.id, member.guild.id, member.top_role.id))
    cursor.execute("""
    INSERT INTO levels (user_id, guild_id, level, xp)
    Values (?, ?, 1, 0)
    """, (member.id, member.guild.id))
    cursor.execute("""
    INSERT INTO xp_tracking (user_id, guild_id, xp_earned, last_reset) 
    VALUES (?, ?, 0, ?)
    """,(member.id, member.guild.id, datetime.utcnow()))