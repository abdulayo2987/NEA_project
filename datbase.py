import sqlite3
from moderation import client

file = "nea.sqlite"

def fill_users():
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    members = list(client.get_all_members())
    for member in members:
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (member.id,))
        exists = cursor.fetchone()[0]
        if not exists:
            cursor.execute("""
                INSERT INTO users (user_id, username, join_date, level)
                VALUES (?, ?, ?, ?)
            """, (member.id, member.global_name, member.joined_at.date(), 0))
        else:
            cursor.execute("""
                UPDATE users
                SET username = ?, join_date = ?, level = ?
                WHERE user_id = ?
            """, (member.global_name, member.joined_at.date(), 0, member.id))
    connection.commit()
    connection.close()

def fill_moderation_stats():
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    members = list(client.get_all_members())
    for member in members:
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (member.id,))
        exists = cursor.fetchone()[0]
        if not exists:
            cursor.execute("""
                    INSERT INTO moderation_stats (user_id, guild_id, top_role_id) 
                    VALUES (?, ?, ?)
                    """, (member.id, member.top_role.id, member.guild.id))

        else:
            cursor.execute("""
            UPDATE moderation_stats
            SET top_role_id = ?, guild_id = ?
            WHERE user_id = ?
            """, (member.top_role.id, member.guild.id, member.id))
    connection.commit()
    connection.close()

def fill_guilds(guild):
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM guilds WHERE guild_id = ?", (guild.id,))
    exists = cursor.fetchone()[0]
    if not exists:
        cursor.execute("""
        INSERT INTO guilds (guild_id, guild_name, owner_id, creation_date) VALUES (?, ?, ?, ?)
        """, (guild.id, guild.name, guild.owner.global_name, guild.created_at.date()))
        print("code ran")
    else:
        cursor.execute("""
        UPDATE guilds
        SET guild_name = ?, owner_id = ?, creation_date = ?
        WHERE guild_id = ?
        """, (guild.name, guild.owner.id, guild.created_at.date(), guild.id))
        print("code ran")
    connection.commit()
    connection.close()

def fill_roles(guild):
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    roles = list(guild.roles)
    for role in roles:
        cursor.execute("SELECT COUNT(*) FROM roles WHERE role_id = ?", (role.id,))
        exists = cursor.fetchone()[0]
        if not exists:
            cursor.execute("""
            INSERT INTO roles (role_id, role_name, guild_id, permissions) 
            VALUES (?, ?, ?, ?)
            """, (role.id, role.name, role.guild.id, role.permissions.value))
        else:
            cursor.execute("""
            UPDATE roles
            SET role_name = ?, guild_id = ?, permissions = ?
            WHERE role_id = ?
            """, (role.id, role.name, role.guild.id, role.permissions.value))
    connection.commit()
    connection.close()

def fill_user_roles():
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    members = list(client.get_all_members())
    for member in members:
        cursor.execute("SELECT COUNT(*) FROM user_roles "
                       "WHERE user_id = ? AND top_role_id = ? AND guild_id = ? ", (member.id, member.top_role.id, member.guild.id))
        exists = cursor.fetchone()[0]
        if not exists:
            if member.top_role:
                cursor.execute("""
                Insert into user_roles (user_id, top_role_id, guild_id)
                VALUES (?, ?, ?)
                """, (member.id, member.top_role.id, member.guild.id))
        else:
            if member.top_role:
                cursor.execute("""
                UPDATE user_roles
                SET top_role_id = ?, guild_id = ?
                WHERE user_id = ?
                """, (member.top_role.id, member.guild.id, member.id))
    connection.commit()
    connection.close()

def fill_database(guild):
    fill_users()
    fill_moderation_stats()
    fill_guilds(guild)
    fill_roles(guild)
    fill_user_roles()