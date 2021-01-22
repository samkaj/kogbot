import discord
import json
import guild_info
from discord.ext import commands
from discord.utils import get
import asyncio
import time
import random

if __name__ == "__main__":
    intent = discord.Intents(messages=True, members=True, guilds=True)
    bot = commands.Bot(command_prefix="!", intents=intent)
    _guilds = {}


    @bot.event
    async def on_ready():
        # create GuildInfo objects for all guilds
        for g in bot.guilds:
            _guilds[g.id] = guild_info.GuildInfo(g)
        print("bot online, sending messages")
        await send_challenge_interval()


    @bot.command()
    async def join(ctx):
        c = ctx.author.voice.channel
        await c.connect()

    @bot.command()
    async def leave(ctx):
        await ctx.voice_client.disconnect()

    def load_from_data(filename):
        with open(f"data/{filename}.json", "r", encoding="utf-8") as doc:
            return json.load(doc)

    async def send_challenge_interval():
        await bot.wait_until_ready()
        g = _guilds.get(801885706611589120) # only for mattias' party
        c = bot.get_channel(g.get_standard_channel_id()).channels[0] # ????
        i = 0
        while True:
            await bot.wait_until_ready()
            role_name = g.get_default_role()
            role = get(g.get_guild().roles, name=role_name)
            i = i + 1
            if random.randint(0,100) == 1:
                user = bot.get_user(g.get_random_user_id())
                await c.send(f'{user.mention} **LEGENDARY** - DELA UT 30 KLUNKAR')
                await asyncio.sleep(100)
            elif random.randint(0,60) == 1:
                feels_bad = [
                    "Roxanne!",
                    "Thunderstruck!",
                    "Vattenfall!"
                ]
                await c.send(f'RARE - {random.choice(feels_bad)}')
            if i%2==0:
                print('everyone')
                challenge_msg = g.get_random_challenge(True) # everyone 
                i = 0
                await c.send(f"{role.mention} - {challenge_msg}")
            else:
                print('random user')
                user = bot.get_user(g.get_random_user_id())
                challenge_msg = g.get_random_challenge(False) # random person
                await c.send(f"{user.mention} - {challenge_msg}")
            await asyncio.sleep(120)


    @bot.command(pass_context=True)
    async def lambo(ctx):
        g = _guilds.get(ctx.guild.id)
        u = bot.get_user(g.get_random_user_id())
        await ctx.send(f'Lambo på {u.mention}!! http://www.studentsanger.se/lambo.html')

    @bot.command(pass_context=True)
    async def challenge(ctx):
        g = _guilds.get(ctx.guild.id)
        user = bot.get_user(g.get_random_user_id())
        challenge_msg = g.get_random_challenge()
        await ctx.send(f"{user.mention} {challenge_msg}")

    @bot.command(pass_context=True)
    async def ping(ctx):
        print("pong")
        await ctx.send(f"pong")

    @bot.event
    async def on_member_join(member):
        g = _guilds.get(member.guild.id)
        role_name = g.get_default_role()
        role = get(member.guild.roles, name=role_name)
        g.add_member(member.name, member.id)
        await member.add_roles(role)
        await member.send(
            f"Jag heter Pierre-Bengt, och är en bot. Du gick nyss med i {g.get_g_name()}.\n{g.get_welcome_message()}\nBörja här: {bot.get_channel(g.get_standard_channel_id()).channels[0].mention} :blue_heart:"
        )

    @bot.command(pass_context=True)
    async def hug(ctx):
        await ctx.send(f"*kramar* {ctx.author.mention} :blue_heart:")



    @bot.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def new_welcome_message(ctx, *args):
        new_message = " ".join(args)
        for g in _guilds:
            g[1].set_new_message("welcome_message", new_message)
            await ctx.send(f'I set the new welcome message to: \n"{new_message}"')
            break
    
    @bot.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def set_default_channel(ctx, arg):
        g = _guilds.get(ctx.guild.id)
        if arg == 'this' or arg == 'here':
            new_id = ctx.channel.id
        else:
            try:
                new_id = int(arg)
                g.set_standard_channel(new_id)
            except ValueError:
                await ctx.send(f"I could not set the new channel :pensive:, *enter a number (or 'here'/'this', if you want to set the channel you're in currently)*")
                return

        await ctx.send(
            f'I set the new default channel to: \n"{ctx.guild.get_channel(new_id).mention}"'
        )

    @bot.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def give_default_role(ctx, *args):
        g = _guilds.get(ctx.guild.id)
        role_name = g.get_default_role()
        role = get(ctx.guild.roles, name=role_name)
        members = ctx.guild.members
        if role:
            if args[0] == 'all':
                members_length = len(members)
                for member in members:
                    await member.add_roles(role)
            else:
                names = [m.name.split('#')[0] for m in members]
                members_length = len(args)
                for arg in args:
                    if arg in names:
                        i = names.index(arg)
                        await members[i].add_roles(role)
                
            await ctx.send(f"Role **{role_name}** was added to {members_length} member(s)")
        else:
            await ctx.send(f'No default role set, use `{ctx.prefix}set_default_role` (case sensitive) to set a default role. :blue_heart:')

    @bot.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def set_default_role(ctx, *args):
        g = _guilds.get(ctx.guild.id)
        a = ' '.join(args)
        found = False
        for role in ctx.guild.roles:
            if role.name == a:
                g.change_data('default_role', a)
                found = True
                break
        if found:
            await ctx.send(f'New default role set to `{a}`')
        else:
            await ctx.send(f'Role not found, try again! (It is case-sensitive)')
                

    bot.run(load_from_data("config")["DISCORD_TOKEN"])
