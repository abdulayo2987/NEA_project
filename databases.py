import sqlite3
file = "NEA_project.db"
connection = sqlite3.connect(file)
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
               user_id VARCHAR,
               username VARCHAR,
               discord_id VARCHAR,
               join_date DATETIME,
               level INTEGER,
               experience_points INTEGER,
               PRIMARY KEY (user_id),
)
""")
#fix table primary key
cursor.execute("""
CREATE TABLE IF NOT EXISTS guilds (
               guild_id VARCHAR,
               guild_name VARCHAR,
               owner_id VARCHAR,
               creation_date DATETIME,
               PRIMARY KEY (guild_id),
               FOREIGN KEY (owner_id) REFERENCES Persons(PersonID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS roles (
               role_id INTEGER,
               role_name VARCHAR,
               guild_id VARCHAR,
               permissions TEXT,
               PRIMARY KEY (role_id),
               FOREIGN KEY (guild_id) REFERENCES guilds(guild_id)
)
""")

#join table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_roles (
               user_role_id INTEGER,
               user_id VARCHAR,
               role_id INTEGER,
               guild_id VARCHAR,
               PRIMARY KEY (user_role_id),
               FOREIGN KEY (user_id) REFERENCES users(user_id)
               FOREIGN KEY (role_id) REFERENCES roles(role_id)
               FOREIGN KEY (guild_id) REFERENCES guilds(guild_id)
""")


#fix table
cursor.execute("""
CREATE TABLE IF NOT EXISTS moderation_stats (
               user_id VARCHAR,
               role_id VARCHAR,
               guild_id VARVHAR,
               warns_count INTEGER DEFAULT 0,
               kicks_count INTEGER DEFAULT 0,
               mutes_count INTEGER DEFAULT 0,
               ban_count INTEGER DEFAULT 0,
               PRIMARY KEY (OrderID),
               FOREIGN KEY (PersonID) REFERENCES Persons(PersonID)
)
""")
#end

cursor.execute("""
CREATE TABLE IF NOT EXISTS moderation_actions (
               moderation_id INTEGER,
               user_id VARCHAR,
               moderator_id VARCHAR,
               guild_id VARCHAR,
               action_type VARCHAR,
               reason TEXT,
               timestamp DATETIME,
               duration INTEGER,
               PRIMARY KEY (moderation_id),
               FOREIGN KEY (user_id) REFERENCES users(usersid)
               FOREIGN KEY (moderator_id) REFERENCES users(user_id)
               FOREIGN KEY (guild_id) REFERENCES guilds(guild_id)
               
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
               event_id INTEGER,
               event_name VARCHAR,
               guild_id VARCHAR,
               created_by VARCHAR,
               start_time DATETIME,
               end_time DATETIME,
               PRIMARY KEY (event_id),
               FOREIGN KEY (guild_id) REFERENCES guilds(guild_id)
               FOREIGN KEY (created_by) REFERENCES users(user_id)
)
""")
#join table
cursor.execute("""
CREATE TABLE IF NOT EXISTS events_participants (
               participant_id INTEGER,
               user_id VARCHAR,
               event_id INTEGER,
               PRIMARY KEY (participant_id),
               FOREIGN KEY (user_id) REFERENCES users(user_ID)
               FOREIGN KEY (event_id) REFERENCES events(user_ID)
               
)
""")



