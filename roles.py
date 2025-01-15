import discord
from functions import new_channel
from moderation import *



async def new_roles_channel(guild):
    channel = await new_channel(guild, "roles")
    await channel.set_permissions(guild.default_role,send_messages=False)

#def role_commands(guild):
#   roles = guild.
#
#    @bot.command(name="add_role", description="Add a nev role into the server")
#    @app_commands.describe(role_name="What is the name of the role you want to add", emoji="What is the emoji of the role you want to add")
#    async def add_role(interaction: discord.Interaction):
#        if punishment[0]:

