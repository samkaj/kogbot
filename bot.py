import discord
import json
from discord.ext import commands

pb = commands.Bot(command_prefix="<")

def load_config():
    with open('data/config.json', 'r', encoding='utf-8') as doc:
        return json.load(doc)


@pb.command()
async def ping(ctx):
    await ctx.send('pong')

@pb.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def set_welcome_message(ctx, *args):
    json_object["WELCOME_MESSAGE"] = ' '.join(args)
    message_file = open('data/messages.json', 'w')
    json.dump(json_object, message_file)
    message_file.close()


@pb.command()
async def DM(ctx, user:'783980654236925964', *, message=None):
    message = message or "This Message is sent via DM"
    await user.send(message)


print('pb is online')
pb.run(load_config()['DISCORD_TOKEN'])