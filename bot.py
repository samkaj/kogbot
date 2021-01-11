import discord
import json
import guild_info
from discord.ext import commands
from discord.utils import get

if __name__ == "__main__":
    intent = discord.Intents(messages=True, members=True, guilds=True)
    bot = commands.Bot(command_prefix="!", intents=intent)
    _guilds = {}

    @bot.event
    async def on_ready():
        # create GuildInfo objects for all guilds
        for g in bot.guilds:
            _guilds[g.id] = guild_info.GuildInfo(g)
        print("bot online")

    def load_from_data(filename):
        with open(f"data/{filename}.json", "r", encoding="utf-8") as doc:
            return json.load(doc)

    @bot.command(pass_context=True)
    async def ping(ctx):
        print("pong")
        await ctx.send("pong")

    @bot.event
    async def on_member_join(member):
        g = _guilds.get(member.guild.id)
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
    async def set_default_channel_id(ctx, arg):
        try:
            new_id = int(arg)
            for g in _guilds:
                g[1].set_new_message("standard_channel_id", new_id)
                await ctx.send(
                    f'I set the new default channel ID to: \n"{ctx.guild.get_channel(new_id).mention}"'
                )
        except TypeError:
            await ctx.send(f"I could not set the new ID, try entering a number!")

    # TODO: fix this
    @bot.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def give_default_role(ctx):
        # for g in _guilds:
        #     if(g[0].id == ctx.guild.id):
        #         role_name = g[1].get_msg_from_input("DEFAULT_ROLE")
        #         if role_name:
        #             role = get(ctx.guild.roles, name=role_name)
        #             for member in ctx.guild.members:
        #                 await member.add_roles(role)
        await ctx.send("Not yet implemented")

    bot.run(load_from_data("config")["DISCORD_TOKEN"])
