import discord
#import generateMsg

from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
from dotenv import load_dotenv
import os

# Write a discord bot that uses gpt-3 to generate text.
# The bot should be able to generate text from a single command.

intents = discord.Intents.default()
intents.members = True

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


'''
client = Client()
client.run(os.getenv("DISCORD_TOKEN"))
'''

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Ready")

@bot.command(pass_context=True)
async def join(ctx):
    author = ctx.message.author
    channel = author.voice.channel
    await channel.connect()

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user: return
    if not message.content[0] == "!": return 
    # Placeholder. When deploying: generateMsg.generate(message.content)

    command = message.content[1:]
    if command[0] == "!":
        response = "Uwu!"
        await message.channel.send(response)
    
    elif command[0] == "?":
        response = "UwU!"
        await message.channel.send(response)

    elif command[0] == ";":
        response = """Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
        """
        await message.channel.send(response)

    

bot.run(os.getenv("DISCORD_TOKEN"))

