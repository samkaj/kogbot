import discord
import json
from discord.ext import commands

intent = discord.Intents(messages=True, members=True)

client = commands.Bot(command_prefix="!", intents=intent)

def load_from_data(filename):
    with open(f'data/{filename}.json', 'r', encoding='utf-8') as doc:
        return json.load(doc)

@client.command()
async def ping(ctx):
    print('pong')
    await ctx.send('pong')

@client.command()
async def set_default_channel(ctx, *args):
    data = load_from_data('messages')
    data["DEFAULT_CHANNEL_ID"] = int(' '.join(args))
    with open("data/messages.json", "w") as doc:
        json.dump(data, doc)

@client.command()
async def set_welcome_message(ctx, *args):
    data = load_from_data('messages')
    data["WELCOME_MESSAGE"] = int(' '.join(args))
    with open("data/messages.json", "w") as doc:
        json.dump(data, doc)
    
@client.event
async def on_member_join(member):
    messages = load_from_data('messages')
    text_channel = messages['DEFAULT_CHANNEL_ID']
    await member.send(f"{messages['WELCOME_MESSAGE']}\nBörja här: <#{text_channel}>!")




print('Pierre-Bengt is online!')
client.run(load_from_data('config')['DISCORD_TOKEN'])