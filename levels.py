import random
from datetime import datetime
from typing import Optional
from moderation import *

file = "nea.sqlite"

async def new_levels_channel(guild):
    await new_channel(guild, "levels")
    channel = discord.utils.get(guild.channels, name="levels")
    await channel.set_permissions(guild.default_role, send_messages=True)
    for i in range(5):
        new_role = await interaction.guild.create_role(name=f"rank_{i}", colour="pink")
        connection = sqlite3.connect("nea.sqlite")
        cursor = connection.cursor()
        cursor.execute("""
                    INSERT INTO roles (role_id, role_name, guild_id, permissions) 
                    VALUES (?, ?, ?, ?)
                    """, (new_role.id, new_role.name, new_role.guild.id, new_role.permissions.value))
        connection.commit()
        connection.close()

async def add_level_role(message, current_level):
    guild = message.guild
    if current_level == 1:
        role = discord.utils.get(guild.roles, name="rank_1")
        await message.author.add_roles(role)
    elif 2 <= current_level < 10:
        role = discord.utils.get(guild.roles, name="rank_2")
        await message.author.add_roles(role)
    elif 10 <= current_level < 20:
        role = discord.utils.get(guild.roles, name="rank_3")
        await message.author.add_roles(role)
    elif 20 <= current_level < 50:
        role = discord.utils.get(guild.roles, name="rank_4")
        await message.author.add_roles(role)
    elif 50 <= current_level < 100:
        role = discord.utils.get(guild.roles, name="rank_5")
        await message.author.add_roles(role)
    cursor.execute("""
            UPDATE user_roles
            SET top_role_id = ?
            WHERE user_id = ? AND guild_id = ?
            """, (message.author.top_role.id, message.author.id, message.guild.id))

async def message_xp(message: Message):
    xp_to_add = random.randint(15,25)
    xp_limit = 1000
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT xp_earned, last_reset 
        FROM xp_tracking
        WHERE user_id = ? AND guild_id = ?
    """, (message.author.id, message.guild.id))
    result = cursor.fetchone()
    current_time = datetime.utcnow()
    if result is None:
        xp_earned, last_reset = 0, current_time  # Default values
    else:
        xp_earned, last_reset = result
    last_reset = datetime.strptime(last_reset, "%Y-%m-%d %H:%M:%S.%f")
    if current_time - last_reset >= timedelta(hours=1):
        cursor.execute("""
                    UPDATE xp_tracking
                    SET xp_earned = ?, last_reset = ?
                    WHERE user_id = ? AND guild_id = ?
                """, (xp_to_add, current_time, message.author.id, message.guild.id))
        cursor.execute("""
                        SELECT level, xp
                        FROM levels
                        WHERE user_id = ? AND guild_id = ?      
                """, (message.author.id, message.guild.id))
        result = cursor.fetchone()
        level, xp = result
        xp = int(xp)
        xp = xp + xp_to_add
        current_level = int(level)
        next_level_xp = 5 / 6 * current_level * (2 * current_level ^ 2 + 27 * current_level + 91)
        if xp > next_level_xp:
            current_level = current_level + 1
            await add_level_role(message, current_level)
            await message.channel.send(f"<@{message.author.id}> has reached level {current_level}. well done ")
        else:
            await add_level_role(message, current_level)
        cursor.execute("""
                UPDATE levels
                SET xp = ?, level = ?
                WHERE user_id = ? AND guild_id = ?
                """, (xp + xp_to_add, current_level, message.author.id, message.guild.id))
    elif xp_earned+xp_to_add <= xp_limit:
        cursor.execute("""
                    UPDATE xp_tracking
                    SET xp_earned = ?
                    WHERE user_id = ? AND guild_id = ?
                """, (xp_to_add+xp_earned, message.author.id, message.guild.id))
        cursor.execute("""
                SELECT level, xp
                FROM levels
                WHERE user_id = ? AND guild_id = ?      
        """,(message.author.id, message.guild.id))
        result = cursor.fetchone()
        level, xp = result
        xp = int(xp)
        xp = xp + xp_to_add
        current_level = int(level)
        next_level_xp = 5/6*current_level*(2*current_level^2+27*current_level+91)
        if xp > next_level_xp:
            current_level = current_level + 1
            await message.channel.send(f"<@{message.author.id}> has reached level {current_level}. well done ")
        cursor.execute("""
        UPDATE levels
        SET xp = ?, level = ?
        WHERE user_id = ? AND guild_id = ?
        """, (xp+xp_to_add, current_level, message.author.id, message.guild.id))
    connection.commit()
    connection.close()

def leveling_commands():

    @bot.command(name="level", description="show current level")
    @app_commands.describe(member="Member which you'd like to view")
    async def level(interaction: discord.Interaction, member: Optional[discord.Member] = None):
        if member:
            connection = sqlite3.connect(file)
            cursor = connection.cursor()
            cursor.execute("""
                                    SELECT level
                                    FROM levels
                                    WHERE user_id = ? AND guild_id = ?      
                                    """, (member.id, interaction.guild.id))
            level = cursor.fetchone()[0]
            connection.close()
            await interaction.response.send_message(f"<@{member.id}>'s level is {level}, they need to send more messages to level up 😊")
        else:
            connection = sqlite3.connect(file)
            cursor = connection.cursor()
            cursor.execute("""
                                    SELECT level
                                    FROM levels
                                    WHERE user_id = ? AND guild_id = ?      
                                    """, (interaction.user.id, interaction.guild.id))
            level = cursor.fetchone()[0]
            connection.close()
            await interaction.response.send_message(f"your level is {level}, send more messages to level up 😊")

    @bot.command(name="xp", description="show current xp")
    @app_commands.describe(member="Member which you'd like to view")
    async def xp_total(interaction: discord.Interaction, member: Optional[discord.Member] = None):
        if member:
            connection = sqlite3.connect(file)
            cursor = connection.cursor()
            cursor.execute("""
                                        SELECT xp
                                        FROM levels
                                        WHERE user_id = ? AND guild_id = ?      
                                        """, (member.id, interaction.guild.id))
            xp = cursor.fetchone()[0]
            connection.close()
            await interaction.response.send_message(
                f"<@{member.id}> has {xp} xp, they need to send more messages to increase it 😊")
        else:
            connection = sqlite3.connect(file)
            cursor = connection.cursor()
            cursor.execute("""
                                        SELECT xp
                                        FROM levels
                                        WHERE user_id = ? AND guild_id = ?      
                                        """, (interaction.user.id, interaction.guild.id))
            xp = cursor.fetchone()[0]
            connection.close()
            await interaction.response.send_message(f"you have {xp} xp, send more messages to increase it 😊")

    @bot.command(name="leaderboard", description="shows the top 10 people with the most xp")
    async def leaderboard(interaction: discord.Interaction):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT user_id, xp
        FROM levels
        ORDER BY xp DESC LIMIT 10
        """)
        top_10 = cursor.fetchall()
        connection.close()
        embed = discord.Embed(
            title="Leaderboard",
            color=discord.Color.blue()  # Choose any color
        )
        leaderboard = "\n".join([f"<@{client.get_user(user[0]).id}> has {user[1]} xp" for user in top_10])
        embed.description = f"{leaderboard}"
        await interaction.response.send_message(embed=embed)

    @bot.command(name="xp_next", description="shows required amount of xp needed till next level")
    @app_commands.describe(member="Member which you'd like to view")
    async def xp_next(interaction: discord.Interaction, member: Optional[discord.Member] = None):
        if member:
            connection = sqlite3.connect(file)
            cursor = connection.cursor()
            cursor.execute("""
                                    SELECT level, xp
                                    FROM levels
                                    WHERE user_id = ? AND guild_id = ?      
                                    """, (member.id, interaction.guild.id))
            level = int(cursor.fetchone()[0]) + 1
            connection.close()
            next_level = int(5 / 6 * level * (2 * level ^ 2 + 27 * level + 91))
            next_xp = next_level - int(cursor.fetchone()[1])
            await interaction.response.send_message(
                f"<@{member.id}> needs {next_xp} xp to get to level {level}, tell them to keep sending messages 😋")

        else:
            connection = sqlite3.connect(file)
            cursor = connection.cursor()
            cursor.execute("""
                                SELECT level
                                FROM levels
                                WHERE user_id = ? AND guild_id = ?      
                                """, (interaction.user.id, interaction.guild.id))
            level = int(cursor.fetchone()[0]) + 1
            connection.close()
            next_xp = int(5/6*level*(2*level^2+27*level+91))
            await interaction.response.send_message(f"you need {next_xp} xp to get to level {level}, keep sending messages 😋")

    @bot.command(name="xp_add", description="adds xp to specified user")
    @app_commands.describe(xp="xp to add", member="Member which you'd like to add xp to")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def xp_add(interaction: discord.Interaction, xp: int, member: discord.Member):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute("""
                                SELECT xp
                                FROM levels
                                WHERE user_id = ? AND guild_id = ?      
                                """, (member.id, interaction.guild.id))
        previous_xp = cursor.fetchone()[0]
        new_xp = xp + previous_xp
        for i in range(100):
            j = i - 1
            level = 5/6*i*(2*i^2+27*i+91)
            previous_level = 5/6*j*(2*j^2+27*j+91)
            if previous_level < new_xp < level:
                level = i
                cursor.execute("""
                UPDATE levels
                SET xp = ?, level = ?
                WHERE user_id = ? AND guild_id = ?      
                """,(new_xp, level, member.id, interaction.guild.id) )
                connection.commit()
                connection.close()
                break
        await interaction.response.send_message(f"{xp} xp has been added to <@{member.id}>")

    @bot.command(name="xp_remove", description="removes xp from specified user")
    @app_commands.describe(xp="xp to remove", member="Member which you'd like to remove xp from")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def xp_remove(interaction: discord.Interaction, xp: int, member: discord.Member):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute("""
                                    SELECT xp
                                    FROM levels
                                    WHERE user_id = ? AND guild_id = ?      
                                    """, (member.id, interaction.guild.id))
        previous_xp = cursor.fetchone()[0]
        new_xp = previous_xp - xp
        if new_xp < 0:
            new_xp = 0
            cursor.execute("""
                                UPDATE levels
                                SET xp = ?, level = 1
                                WHERE user_id = ? AND guild_id = ?      
                                """, (new_xp, member.id, interaction.guild.id))
        else:
            for i in range(100):
                j = i - 1
                level = 5 / 6 * i * (2 * i ^ 2 + 27 * i + 91)
                previous_level = 5 / 6 * j * (2 * j ^ 2 + 27 * j + 91)
                if previous_level < new_xp < level:
                    level = i
                    cursor.execute("""
                        UPDATE levels
                        SET xp = ?, level = ?
                        WHERE user_id = ? AND guild_id = ?      
                        """, (new_xp, level, member.id, interaction.guild.id))
                    break
        connection.commit()
        connection.close()
        await interaction.response.send_message(f"{xp} xp has been removed from <@{member.id}>")

    @bot.command(name="xp_reset", description="resets a users xp")
    @app_commands.describe(member="Member which you'd like to remove xp from")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def xp_reset(interaction: discord.Interaction, member: discord.Member):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE levels
        SET xp = 0, level = 1
        WHERE user_id = ? AND guild_id = ?      
        """, (member.id, interaction.guild.id))
        connection.commit()
        connection.close()
        await interaction.response.send_message(f"<@{member.id}>'s xp has been reset. 😥")

    @bot.command(name="set_level", description="sets a users level")
    @app_commands.describe(level="level that user will be at", member="Member which you'd like to change level")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def set_level(interaction: discord.Interaction, level: int, member: discord.Member):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        xp = 5 / 6 * level * (2 * level ^ 2 + 27 * level + 91)
        cursor.execute("""
        UPDATE levels
        SET level = ?, xp = ?
        WHERE user_id = ? AND guild_id = ?
        """, (level, xp, member.id, interaction.guild.id))
        connection.commit()
        connection.close()
        await interaction.response.send_message(f"<@{member.id}>'s level has been set to {level}")

    @bot.command(name="set_xp", description="sets a users xp")
    @app_commands.describe(xp="how much xp user will have", member="Member which you'd like to change xp points")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def set_xp(interaction: discord.Interaction, xp: int, member: discord.Member):
        connection = sqlite3.connect(file)
        cursor = connection.cursor()
        for i in range(100):
            j = i - 1
            level = 5/6*i*(2*i^2+27*i+91)
            previous_level = 5/6*j*(2*j^2+27*j+91)
            if previous_level < xp < level:
                level = i
                cursor.execute("""
                        UPDATE levels
                        SET level = ?, xp = ?
                        WHERE user_id = ? AND guild_id = ?
                        """, (level, xp, member.id, interaction.guild.id))
        connection.commit()
        connection.close()
        await interaction.response.send_message(f"<@{member.id}>'s xp points has been set to {xp}")
