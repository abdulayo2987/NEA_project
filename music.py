import wavelink
from moderation import *
from ytmusicapi import YTMusic

ytmusic = YTMusic()

queue = []

def search_music(song:str, artist:str = None):
    query = f"{song} {artist}" if artist else song
    results = ytmusic.search(query, filter="songs", limit=1)
    if results:
        song_title = results[0]['title']
        song_artist = results[0]['artists'][0]['name']
        return f"ytsearch:{song_title} {song_artist}"
    return None

async def music_setup():
    node = wavelink.Node(uri="lavalink.eu:2333", password="youshallnotpass")
    await wavelink.Pool.connect(client=bot, nodes=[node])
    await wavelink.NodePool.create_node(
        bot=bot,
        host="lavalink.eu",
        port=2333,
        password="youshallnotpass",
        region="europe"
    )


def music_commands():

    @bot.command(name="play", description="plays music")
    async def play(interaction: discord.Interaction):
        if not interaction.user.voice or not interaction.user.voice.channel:
            return await interaction.response.send_message("You need to join a voice channel first.")

        channel = interaction.user.voice.channel
        vc: wavelink.Player = await wavelink.NodePool.get_node().get_player(interaction.guild)

        if not vc.is_connected():
            await vc.connect(channel.id)

        query = "skyfall"
        tracks = await wavelink.YouTubeTrack.search(query)
        if not tracks:
            return await interaction.response.send_message("No results found.", ephemeral=True)

        track = tracks[0]
        await vc.play(track)
        await interaction.response.send_message(f"Now playing: **{track.title}**")


    @bot.command(name="pause", description="pauses music")
    async def pause(interaction: discord.Interaction):
        pass

    @bot.command(name="skip", description="skips to next song")
    async def skip(interaction: discord.Interaction):
        pass

    @bot.command(name="remove_queue", description="removes a song from queue")
    async def remove_queue(interaction: discord.Interaction):
        pass

    @bot.command(name="add_queue", description="adds song to queue")
    @app_commands.describe(song="The song to add", artist="The artist of the song")
    async def add_queue(interaction: discord.Interaction, song:str, artist:str = None):
        pass

    @bot.command(name="queue", description="shows queue")
    async def show_queue(interaction: discord.Interaction):
        await interaction.response.send_message(f"Queue: {query}")

    @bot.command(name="empty_queue", description="removes all songs from the queue")
    async def empty_queue(interaction: discord.Interaction):
        pass