import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # Subscribe to member events
intents.presences = True  # Subscribe to presence events
intents.message_content = True  # Subscribe to message content

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command()
async def hello(ctx):
    await ctx.send('Halo Tuan!')


@bot.command()
async def hi(ctx):
    await ctx.send('hello world!')

    

token = 'ganti-dengan-token'
bot.run(token)
