from functions import new_channel
from moderation import *

role_emojis={
    "member":"😊"  #store in premade text file if enough time 
}

async def new_roles_channel(guild):
    channel = await new_channel(guild, "roles")
    global channel_id
    channel_id = channel.id
    await channel.set_permissions(guild.default_role,send_messages=False)


async def role_autocomplete(interaction: discord.Interaction, current: str):
    roles = interaction.guild.roles
    return [
        app_commands.Choice(name=role.name, value=str(role.id))
        for role in roles
        if current.lower() in role.name.lower()
    ]

async def user_role_autocomplete(current: str, user: discord.Member):
    roles = user.roles
    return [
        app_commands.Choice(name=role.name, value=str(role.id))
        for role in roles
        if current.lower() in role.name.lower()
    ]

def role_commands():

    @bot.command(name="new_role", description="Add a new role into the server")
    @app_commands.describe(role_name="What is the name of the role you want to add",
                           emoji="What is the emoji of the role you want to add(windows key + '.')",
                           colour="What colour do you want this role to be")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def new_role(interaction: discord.Interaction, role_name: str, emoji: str, colour: str):
        try:
            colour = getattr(discord.Color, colour.lower())()
        except AttributeError:
            await interaction.response.send_message("Please us a valid colour name")

        role_exists = discord.utils.get(interaction.guild.roles, name=role_name)
        if role_exists:
            await interaction.response.send_message(f"a role with the name {role_name} already exists")
        else:
            new_role = await interaction.guild.create_role(name=role_name, colour=colour)
            await interaction.response.send_message(f"role '<@&{new_role.id}>' has been added to the server", ephemeral=False)
            role_emojis[new_role.name] = emoji
            connection = sqlite3.connect("nea.sqlite")
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO roles (role_id, role_name, guild_id, permissions) 
            VALUES (?, ?, ?, ?)
            """, (new_role.id, new_role.name, new_role.guild.id, new_role.permissions.value ))
            connection.commit()
            connection.close()

    @bot.command(name="list_all_roles", description="Lists all roles in the server")
    async def list_all_roles(interaction: discord.Interaction):
        roles = interaction.guild.roles
        role_info = "\n".join([f"<@&{role.id}>  {role.id}" for role in roles])
        embed = discord.Embed(colour=discord.Colour.green())
        embed.description = f"{role_info}"
        await interaction.response.send_message(embed=embed)

    @bot.command(name="delete_role", description="Remove a role from the server")
    @app_commands.describe(role="What is the name of the role you want to remove",)
    @app_commands.checks.has_permissions(manage_roles=True)
    async def delete_role(interaction: discord.Interaction, role: str):
        role = interaction.guild.get_role(int(role))
        connection = sqlite3.connect("nea.sqlite")
        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM roles
        WHERE role_id = ?
        """, (role.id,))
        connection.commit()
        connection.close()
        if role.name in role_emojis:
            del role_emojis[role.name]
        try:
            await role.delete()
        except discord.Forbidden:
            await interaction.response.send_message(f"I do not have permission to delete <@&{role.id}>")
            return
        await interaction.response.send_message(f"{role.name} has been removed from the server")
    @delete_role.autocomplete("role")
    async def delete_role_autocomplete(interaction: discord.Interaction, current: str):
        return await role_autocomplete(interaction, current)

    @bot.command(name="add_role_to_member", description="Add a role to a member in the server")
    @app_commands.describe(user="Who do you want me to add the role to", role="What is the name of the role you want to add")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def add_role_to_member(interaction: discord.Interaction, user: discord.Member, role: str):
        role = interaction.guild.get_role(int(role))
        try:
            await user.add_roles(role)
        except discord.Forbidden:
            await interaction.response.send_message(f"I do not have permission to add <@&{role.id}>")
            return
        connection = sqlite3.connect("nea.sqlite")
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE user_roles
        SET top_role_id = ?
        WHERE user_id = ? AND guild_id = ?
        """, (user.top_role.id, user.id, role.guild.id))
        connection.commit()
        connection.close()
        await interaction.response.send_message(f"{user.mention} has been given the role <@&{role.id}>")
    @add_role_to_member.autocomplete("role")
    async def add_role_autocomplete(interaction: discord.Interaction, current: str):
        return await role_autocomplete(interaction, current)

    @bot.command(name="remove_role_from_member", description="remove a role from a member in the server")
    @app_commands.describe(user="Who do you want me to remove the role from",
                           role="What is the name of the role you want to remove")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remove_role_from_member(interaction: discord.Interaction, user: discord.Member, role: str):
        role = interaction.guild.get_role(int(role))
        try:
            await user.remove_roles(role)
        except discord.Forbidden:
            await interaction.response.send_message(f"I do not have permission to remove <@&{role.id}> from {user.mention}")
            return
        connection = sqlite3.connect("nea.sqlite")
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE user_roles
            SET top_role_id = ?
            WHERE user_id = ? AND guild_id = ?
            """, (user.top_role.id, user.id, role.guild.id))
        connection.commit()
        connection.close()
        await interaction.response.send_message(f"{user.mention} has been stripped of the role <@&{role.id}>")
    @remove_role_from_member.autocomplete("role")
    async def remove_role_autocomplete(interaction: discord.Interaction, current: str):
        user = interaction.user
        return await user_role_autocomplete(current, user)

    @bot.command(name="change_role_emoji", description="Change the emoji of a role in the server")
    @app_commands.describe(role="What is the name of the role you want to change", emoji="What emoji do you want this emoji to have")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def change_role_emoji(interaction: discord.Interaction, role: str, emoji: str):
        role = interaction.guild.get_role(int(role))
        role_emojis[role.name] = emoji
        await interaction.response.send_message(f"<@&{role.id}>'s emoji has been changed to {emoji}")
    @change_role_emoji.autocomplete("role")
    async def change_role_emoji_autocomplete(interaction: discord.Interaction, current: str):
        return await role_autocomplete(interaction, current)

    @bot.command(name="change_role_color", description="Change the color of the role in the server")
    @app_commands.describe(role="What is the name of the role you want to change",
                           colour="What colour do you want this role to be")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def change_role_color(interaction: discord.Interaction, role: str, colour: str):
        try:
            color = getattr(discord.Color, colour.lower())()
        except AttributeError:
            await interaction.response.send_message("Please us a valid colour name")
        role = interaction.guild.get_role(int(role))
        await role.edit(colour=color)
        await interaction.response.send_message(f"<@&{role.id}>'s colour has been changed to {colour}")

    @change_role_color.autocomplete("role")
    async def change_role_color_autocomplete(interaction: discord.Interaction, current: str):
        return await role_autocomplete(interaction, current)

    @bot.command(name="add_role_to_all_members", description="Add a role to a all members in the server")
    @app_commands.describe(role="What is the name of the role you want to add to everyone")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def add_role_to_all_members(interaction: discord.Interaction, role: str):
        role = interaction.guild.get_role(int(role))
        connection = sqlite3.connect("nea.sqlite")
        cursor = connection.cursor()
        for member in interaction.guild.members:
            try:
                await member.add_roles(role)
            except discord.Forbidden:
                await interaction.response.send_message(f"I do not have permission to add <@&{role.id}>")
                return
            cursor.execute("""
                    UPDATE user_roles
                    SET top_role_id = ?
                    WHERE user_id = ? AND guild_id = ?
                    """, (member.top_role.id, member.id, role.guild.id))
        connection.commit()
        connection.close()
        await interaction.response.send_message(f"everyone has been given the role <@&{role.id}>")
    @add_role_to_all_members.autocomplete("role")
    async def add_role_to_all_members_autocomplete(interaction: discord.Interaction, current: str):
        return await role_autocomplete(interaction, current)

    @bot.command(name="remove_role_from_all_members", description="Remove a role in a all members in the server")
    @app_commands.describe(role="What is the name of the role you want to remove")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remove_role_from_all_members(interaction: discord.Interaction, role: str):
        role = interaction.guild.get_role(int(role))
        connection = sqlite3.connect("nea.sqlite")
        cursor = connection.cursor()
        for member in interaction.guild.members:
            try:
                await member.remove_roles(role)
            except discord.Forbidden:
                await interaction.response.send_message(f"I do not have permission to remove <@&{role.id}>")
                return
            cursor.execute("""
                            UPDATE user_roles
                            SET top_role_id = ?
                            WHERE user_id = ? AND guild_id = ?
                            """, (member.top_role.id, member.id, role.guild.id))
        connection.commit()
        connection.close()
        await interaction.response.send_message(f"everyone has been stripped of the role <@&{role.id}>")
    @remove_role_from_all_members.autocomplete("role")
    async def remove_role_from_all_members_autocomplete(interaction: discord.Interaction, current: str):
        return await role_autocomplete(interaction, current)

    @bot.command(name="add_role_to_existing_role", description="give everyone with a specific role another role")
    @app_commands.describe(existing_role="what role do you want to add to",role_to_add="What is the name of the role you want to add to everyone")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def add_role_to_existing_role(interaction: discord.Interaction, existing_role: str, role_to_add: str):
        existing_role = interaction.guild.get_role(int(existing_role))
        role_to_add = interaction.guild.get_role(int(role_to_add))
        members_with_role = [member for member in interaction.guild.members if existing_role in member.roles]
        if not members_with_role:
            await interaction.response.send_message(f"No members found with the {existing_role.name} role.")
            return
        connection = sqlite3.connect("nea.sqlite")
        cursor = connection.cursor()
        for member in members_with_role:
            try:
                await member.add_roles(role_to_add)
            except discord.Forbidden:
                await interaction.response.send_message(f"I do not have permission to add <@&{role_to_add.id}>")
                return
            cursor.execute("""
                        UPDATE user_roles
                        SET top_role_id = ?
                        WHERE user_id = ? AND guild_id = ?
                        """, (member.top_role.id, member.id, role_to_add.guild.id))
        connection.commit()
        connection.close()
        await interaction.response.send_message(f"everyone with the <@&{existing_role.id}> role has been given the role <@&{role_to_add.id}>")
    @add_role_to_existing_role.autocomplete("existing_role")
    async def add_role_to_existing_role_autocomplete(interaction: discord.Interaction, current: str):
        return await role_autocomplete(interaction, current)
    @add_role_to_existing_role.autocomplete("role_to_add")
    async def add_role_to_existing_role_autocomplete(interaction: discord.Interaction, current: str):
        return await role_autocomplete(interaction, current)

    @bot.command(name="remove_all_roles", description="Remove all roles from a member")
    @app_commands.describe(user="who do you want to remove roles from")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remove_all_roles(interaction: discord.Interaction, user: discord.Member):
        roles = user.roles
        for role in roles:
            if role.name != "@everyone":
                try:
                    await user.remove_roles(role)
                except discord.Forbidden:
                    await interaction.response.send_message(f"I do not have permission to remove <@&{role.id}>")
                    return
        await interaction.response.send_message(f"{user.mention} has been stripped of all roles")
        connection = sqlite3.connect("nea.sqlite")
        cursor = connection.cursor()
        cursor.execute("""
                                UPDATE user_roles
                                SET top_role_id = ?
                                WHERE user_id = ? AND guild_id = ?
                                """, (user.top_role.id, user.id, user.guild.id))
        connection.commit()
        connection.close()

    @bot.command(name="add_role_to_all_humans", description="Add a role to a all humans in the server")
    @app_commands.describe(role="What is the name of the role you want to add to everyone")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def add_role_to_all_humans(interaction: discord.Interaction, role: str):
        role = interaction.guild.get_role(int(role))
        connection = sqlite3.connect("nea.sqlite")
        cursor = connection.cursor()
        for member in interaction.guild.members:
            if member.bot:
                return
            else:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    await interaction.response.send_message(f"I do not have permission to add <@&{role.id}>")
                    return
                cursor.execute("""
                            UPDATE user_roles
                            SET top_role_id = ?
                            WHERE user_id = ? AND guild_id = ?
                            """, (member.top_role.id, member.id, role.guild.id))
        connection.commit()
        connection.close()
        await interaction.response.send_message(f"everyone has been given the role <@&{role.id}>")
    @add_role_to_all_humans.autocomplete("role")
    async def add_role_to_all_humans_autocomplete(interaction: discord.Interaction, current: str):
        return await role_autocomplete(interaction, current)

    @bot.command(name="remove_role_from_all_humans", description="Remove a role in a all humans in the server")
    @app_commands.describe(role="What is the name of the role you want to remove")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remove_role_from_all_humans(interaction: discord.Interaction, role: str):
        role = interaction.guild.get_role(int(role))
        connection = sqlite3.connect("nea.sqlite")
        cursor = connection.cursor()
        for member in interaction.guild.members:
            if member.bot:
                return
            else:
                try:
                    await member.remove_roles(role)
                except discord.Forbidden:
                    await interaction.response.send_message(f"I do not have permission to remove <@&{role.id}>")
                    return
                cursor.execute("""
                                    UPDATE user_roles
                                    SET top_role_id = ?
                                    WHERE user_id = ? AND guild_id = ?
                                    """, (member.top_role.id, member.id, role.guild.id))
            connection.commit()
        connection.close()
        await interaction.response.send_message(f"everyone has been stripped of the role <@&{role.id}>")
    @remove_role_from_all_humans.autocomplete("role")
    async def remove_role_from_all_humans_autocomplete(interaction: discord.Interaction, current: str):
        return await role_autocomplete(interaction, current)

    @bot.command(name="welcome_message", description="sends a welcome message that users can react to to get a role")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def welcome_message(interaction: discord.Interaction):
        channel = discord.utils.get(interaction.guild.channels, name="posts")
        if interaction.channel.id != channel.id:
            await interaction.respone.send_message(f"this command can only be usen in the roles channel")
        else:
            role_info = "\n".join([f"{emoji} -{role}" for role, emoji in role_emojis.items()])
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.description = f"{role_info}"
            message = await interaction.channel.send(embed=embed)
            await interaction.response.send_message(f"react to the following message with corresponding emoji for role")
            for emoji in role_emojis.values():
                try:
                    await message.add_reaction(emoji)
                    global welcome_message_id
                    welcome_message_id = message.id
                    return welcome_message_id
                except discord.HTTPException as e: #cannot add reaction
                    if e.code == 10014:
                        await interaction.response.send_message("one or more of the emojis you have added is not an emoji")
                    return

    @client.event
    async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
        if reaction.message.id == welcome_message_id:
            role_name = next((k for k, role in role_emojis.items() if role == reaction.emoji), None)
            role = user.guild.get_role(int(role_name))
            try:
                await user.add_roles(role)
            except discord.Forbidden:
                await reaction.channel.send_message(f"I do not have permission to add <@&{role.id}>")
                return
            connection = sqlite3.connect("nea.sqlite")
            cursor = connection.cursor()
            cursor.execute("""
            UPDATE user_roles
            SET top_role_id = ?
            WHERE user_id = ? AND guild_id = ?
            """, (user.top_role.id, user.id, role.guild.id))
            connection.commit()
            connection.close()


    @client.event
    async def on_reaction_remove(reaction: discord.Reaction, user: discord.User):
        if reaction.message.id == welcome_message_id:
            role_name = next((k for k, role in role_emojis.items() if role == reaction.emoji), None)
            role = user.guild.get_role(int(role_name))
            try:
                await user.remove_roles(role)
            except discord.Forbidden:
                await reaction.channel.send_message(f"I do not have permission to remove <@&{role.id}>")
                return
            connection = sqlite3.connect("nea.sqlite")
            cursor = connection.cursor()
            cursor.execute("""
            UPDATE user_roles
            SET top_role_id = ?
            WHERE user_id = ? AND guild_id = ?
            """, (user.top_role.id, user.id, role.guild.id))
            connection.commit()
            connection.close()
