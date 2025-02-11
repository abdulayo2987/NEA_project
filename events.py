from moderation import *
from datetime import datetime

file = "nea.sqlite"

def event_commands():

    @bot.command(name="new_event", description="creates a new event")
    @app_commands.describe(event="what would you like to call the event",  date="what date is the event", time="what time is the event", location="where is the event")
    async def new_event(interaction: discord.Interaction, event: str, date: str, time: str, location: str):
        pass

    @bot.command(name="delete_event", description="deletes an event")
    @app_commands.describe(event="name of the event you want to remove")
    async def new_event(interaction: discord.Interaction, ):#options for all current events
        pass

    @bot.command(name="edit_event", description="changes a part of an existing event")
    @app_commands.describe(event="name of the event you want to change", date="what date is the new event", time="what time is the new event")
    async def edit_event(interaction: discord.Interaction, event: str, date: str, time: str):
        pass

    @bot.command(name="list_event", description="lists all upcoming events")
    async def list_event(interaction: discord.Interaction):
        pass