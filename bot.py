import discord
import json
from discord.ext import commands
intents = discord.Intents()
intents.members = True

client = commands.Bot(command_prefix="<", intents=intents)

def load_config():
    with open('data/config.json', 'r', encoding='utf-8') as doc:
        return json.load(doc)

@client.command()
async def ping(ctx):
    await ctx.send('pong')

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def set_welcome_message(ctx, *args):
    json_object["WELCOME_MESSAGE"] = ' '.join(args)
    message_file = open('data/messages.json', 'w')
    json.dump(json_object, message_file)
    message_file.close()

@client.event
async def on_member_join(member):
    message_file = open('data/messages.json', 'r')
    message = json.load(message_file)['WELCOME_MESSAGE']
    await member.send(message)

client.run(load_config()['DISCORD_TOKEN'])
print('Pierre-Bengt is online!')