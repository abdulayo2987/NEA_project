import sqlite3
import os
from pathlib import Path
from moderation import client

def fill_users():
    file = "identifier.sqlite"
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

def fill_moderation():
    file = "identifier.sqlite"
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
            print("code ran successfully")
    connection.commit()
    connection.close()
    print("code ran successfully")

def fill_guilds(Guild):
    file = "identifier.sqlite"
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    guild = Guild
    cursor.execute("""
    INSERT INTO guilds (guild_id, guild_name, owner_id, creation_date) VALUES (?, ?, ?, ?)
    """, (guild.id, guild.name, guild.owner.id, guild.created_at))

def fill_roles():
    file = "identifier.sqlite"
    connection = sqlite3.connect(file)
    cursor = connection.cursor()

def fill_database(Guild):
    if os.path.exists("has_run.txt"):
        print("database filled")
    else:
        file_path = Path("has_run.txt")
        with open(file_path, 'w') as file:
            file.write("database filled")
        fill_users()
        fill_moderation()
        fill_guilds(Guild)