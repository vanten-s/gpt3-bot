from click import pass_context
import discord
import generateMsg
import pycountry
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
from dotenv import load_dotenv
import os
from gtts import gTTS
import gtts.langs

# Write a discord bot that uses gpt-3 to generate text.
# The bot should be able to generate text from a single command.

intents = discord.Intents.default()
intents.members = True
lang = "en"
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
async def stop(ctx):
    print("I am trying to stop the annoying sounds!")
    await ResetAudio(ctx)


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



