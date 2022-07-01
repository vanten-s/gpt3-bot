import discord

# Write a discord bot that uses gpt-3 to generate text.
# The bot should be able to generate text from a single command.

intents = discord.Intents.default()
intents.members = True

def generate_text():
    return "This is a test! Why are you reading this?"

# Create a discord client
class Client(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await self.change_presence(activity=discord.Game(name='Generating text...'))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!generate'):
            await message.channel.send(generate_text())


client = Client()
client.run('')

