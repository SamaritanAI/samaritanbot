import discord
from discord.ext import commands
import aiohttp
import asyncio
import os

bot = commands.Bot(description="This my second bot. A lot of work will be going into it. None of this would be possible without you, Sebi. Thanks bro ^_^... I apologise for many of the errors you'll find here.", command_prefix=("s.", "S.", "samaritan.", "Samaritan."), pm_help=True)

@bot.command()
async def ping(ctx):
    """Test the bot's latency"""
    return await ctx.send('Pong! {0}'.format(round(bot.latency,1000)))
    
@bot.command()
async def say(ctx, *, something):
    """Get the bot to say what you want it to say"""
    await ctx.send(something)

@bot.command()
async def ud(ctx, *, term):
    """Search something on Urban Dictionary"""
    async with aiohttp.request("GET", f"http://api.urbandictionary.com/v0/define?term={term}") as res:
        data = await res.json()
    definition = data["list"][0]
    message = f"""
    Word: {definition["word"]}
    Definition: {definition["definition"]}
    Example: {definition["example"]}
    """
    await ctx.send(message)

@bot.command()
async def avatar(ctx, *, user:discord.Member = None):
    """Englarge someone's avatar"""
    user = user or ctx.author
    await ctx.send(user.avatar_url)

@bot.command()
async def emoji(ctx, *, emoji):
    """Enlarges emoji"""
    custom = emoji.split(":")[-1][:-1]
    url = f"https://cdn.discordapp.com/emojis/{custom}.png" 
    await ctx.send(url)

helpcmd = bot.get_command("help")
@helpcmd.after_invoke
async def help_after(ctx):
    await ctx.send("Help has been DM'd.")

@bot.command()
async def spam(ctx, count: int, *, input: commands.clean_content):
    """Sends spam"""
    for i in range(count):
        await ctx.send(input)
        await asyncio.sleep(1)
        if i == 500:
            await ctx.send("Limit Reached")
            break


@bot.listen('on_ready')
@bot.listen('on_connect')
async def get_owner():
    app_info = await bot.application_info()
    bot.owner_id = app_info.owner.id


bot.load_extension('libneko.extras.superuser')
bot.run(os.environ.get("TOKEN"))

