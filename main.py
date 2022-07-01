import discord
import generateMsg
import pycountry
from discord.ext import commands,tasks
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
from dotenv import load_dotenv
import os
from gtts import gTTS
import gtts.langs
import youtube_dl



# youtube-dl settings

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

#youtube-dl bullshit that I don't understand
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""



    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename




# Write a discord bot that uses gpt-3 to generate text.
# The bot should be able to generate text from a single command.

intents = discord.Intents.default()
intents.members = True
lang = "de"
# Create a discord client
class Client(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await self.change_presence(activity=discord.Game(name='Generating text...'))

    async def on_message(self, message: discord.Message):
        if not message.content.startswith("!"): return
        if message.author == self.user:
            return
        
        messageWithOutPrefix = message.content[1:]
        command = messageWithOutPrefix.split()[0]
        arguments = messageWithOutPrefix.split()[1:]
            

        if command == '!':
            # Make the bot look like it's typing
            await message.channel.trigger_typing()
            if len(arguments) == 0:
                await message.channel.send("usage: !generate <text>")
                return
            
            await message.channel.send(generateMsg.generate(" ".join(arguments)))
            # Make the bot look like it's not typing
            await message.channel.trigger_typing()

        elif command == 'egg':
            await message.channel.send('spam')

        elif command == 'spam':
            for i in range(0, 5):
                await message.channel.send('UwU')

            print('spam')

        elif command.lower() == 'SoMeBoDy'.lower():
            await message.channel.send('SoMeBoDy once told me the world is gonna roll me')
            await message.channel.send('I aint the sharpest tool in the shed')
            await message.channel.send('She was looking kind of dumb with her finger and her finger and her thumb')

        elif command == 'join':
            voice_channel = message.author.voice.channel
            
    

load_dotenv()




bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Ready")


hasJoined = False

@bot.command(pass_context=True)
async def join(ctx):
    hasJoined = True
    print("Joining VC")
    author = ctx.message.author
    channel = author.voice.channel
    await channel.connect()

@bot.command(pass_context=True)
async def la(ctx):
    global lang
    
    if not ctx.message.content[4:].strip().lower() in gtts.langs._langs.keys(): return False
    print(" got through the if not")
    print(ctx.message.content[4:].strip().lower())
    
    
    lang = ctx.message.content[4:].strip().lower()

@bot.command(pass_context=True)
async def doit(ctx: discord.ext.commands.context.Context):
    await ResetAudio(ctx)
    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)

    audio_source = discord.FFmpegPCMAudio('yes.mp3')
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)


bot.command(name='play_song', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


async def ResetAudio(ctx: discord.ext.commands.context.Context):
    for x in bot.voice_clients:
        if x.guild != ctx.message.guild: continue
        await x.disconnect()

    author = ctx.message.author
    channel = author.voice.channel
    await channel.connect()


@bot.command(pass_context=True)
async def gen(ctx: discord.ext.commands.context.Context):

    response = generateMsg.generate(ctx.message.content[5:])

    print("Atleast here")
    try:
        await ResetAudio(ctx)

    except:
        print("awww. ANYWAYS I")

    # response = "UWU"

    await ctx.message.channel.send(response)
    guild = ctx.guild
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    
    tts = gTTS(response, lang=lang, slow=False)
    tts.save("no.mp3")

    audio_source = discord.FFmpegPCMAudio('no.mp3')
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)

bot.run(os.getenv("DISCORD_TOKEN"))



