import discord
from discord.ext import commands
import os
import asyncio
from utils.image_processing import preprocess_image
from utils.song_extraction import extract_song_titles
from utils.audio import play_songs, stop_audio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command(name='play', help='Play songs from an image')
async def play_playlist(ctx):
    """
    Extract songs from an image and play them.
    """
    try:
        attachment = ctx.message.attachments[0]
        if any(attachment.filename.endswith(ext) for ext in ['png', 'jpg', 'jpeg']):
            file_path = f'temp/{attachment.filename}'
            await attachment.save(file_path)
            songs = extract_song_titles(file_path)
            print(songs)
            os.remove(file_path)
            if songs:
                await play_songs(ctx, songs)
            else:
                await ctx.send("No valid songs were found in the image. Please try again with a clearer image.")
        else:
            await ctx.send("Invalid file type. Please upload a PNG, JPG, or JPEG file.")
    except asyncio.TimeoutError:
        await ctx.send("You took too long to upload an image. Please try again.")
    except IndexError:
        await ctx.send("Please attach an image containing the playlist.")


@bot.command(name='stop', help='Stop playback and disconnect the bot')
async def stop(ctx):
    """
    Stop the currently playing song, clear the queue, and disconnect the bot.
    """
    await stop_audio(ctx)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


if __name__ == "__main__":
    bot.run(os.environ['DISCORD_BOT_TOKEN'])
