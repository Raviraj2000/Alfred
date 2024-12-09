import yt_dlp as youtube_dl
import discord
import asyncio

YDL_OPTIONS = {
    'format': 'bestaudio',
    'extractaudio': True,
    'audioformat': 'mp3',
    'noplaylist': 'True'
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

vc = None
song_queue = []


async def fetch_audio_url(song):
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{song} audio", download=False)
            return {
                "title": info['entries'][0]['title'],
                "url": info['entries'][0]['url']
            }
        except Exception as e:
            print(f"Could not fetch URL for {song}: {e}")
            return None


async def preload_songs(songs):
    tasks = [fetch_audio_url(song) for song in songs]
    results = await asyncio.gather(*tasks)
    return [result for result in results if result]


async def play_next_song(ctx):
    global vc, song_queue
    if song_queue:
        next_song = song_queue.pop(0)
        try:
            await ctx.send(f"Now playing: {next_song['title']}")
            vc.play(discord.FFmpegPCMAudio(next_song['url'], **FFMPEG_OPTIONS),
                    after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(ctx), ctx.bot.loop))
        except Exception as e:
            await ctx.send(f"Could not play {next_song['title']}: {e}")
            await play_next_song(ctx)
    else:
        await vc.disconnect()
        vc = None


async def play_songs(ctx, songs):
    global vc, song_queue

    if ctx.author.voice is None:
        await ctx.send("You need to be in a voice channel to play songs!")
        return

    await ctx.send("Fetching song URLs...")
    preloaded_songs = await preload_songs(songs)

    song_queue.extend(preloaded_songs)
    await ctx.send(f"Added {len(preloaded_songs)} songs to the queue.")

    if not vc or not vc.is_connected():
        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()
        await play_next_song(ctx)


async def stop_audio(ctx):
    global vc, song_queue
    if vc:
        song_queue.clear()
        vc.stop()
        await vc.disconnect()
        vc = None
        await ctx.send("Playback stopped and disconnected.")
