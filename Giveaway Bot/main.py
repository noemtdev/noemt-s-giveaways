from discord.ext import commands, tasks
import sys
import traceback
import json
import datetime
import time
import random
import asyncio
import discord
from discord import slash_command
import os
from dotenv import load_dotenv

load_dotenv()

bot = discord.Bot()


def convert(time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]


@commands.cooldown(1, 60, commands.BucketType.user)
@bot.slash_command(
    name="start",
    description="Starts a giveaway"
)
@commands.has_permissions(manage_guild=True)
async def start(ctx, duration: str, prize: str, channel: discord.TextChannel):
    tim = convert(duration)

    embed = discord.Embed(color=0x0398d8, title=f"🎉 {prize} giveaway! 🎉",
                          description=f"React with 🎉 below to enter.", timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Hosted by:", value=ctx.author.mention)
    embed.set_footer(
        text=f"React with 🎉 below to enter! Ends in {duration}",
        icon_url="https://cdn.discordapp.com/avatars/352793093105254402/2f8d558788a138479a797c04c7a90640.webp?size=1024")

    await channel.send(f":tada:  **Giveaway Alert** :partying_face:")

    msg = await channel.send(embed=embed)
    em = discord.Embed(color=0x0398d8, title=f"Giveaway started",
                       description=f"Successfully started a giveaway for `{prize}` in `{channel}`")
    em.set_footer(
        text=f"This giveaway will end in {duration}.",
        icon_url="https://cdn.discordapp.com/avatars/352793093105254402/2f8d558788a138479a797c04c7a90640.webp?size=1024")
    await ctx.respond(embed=em, ephemeral=True)
    await msg.add_reaction("🎉")

    await asyncio.sleep(tim)

    new_msg = await ctx.channel.fetch_message(msg.id)

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))

    winner = random.choice(users)

    em = discord.Embed(
        color=0x0398d8, title="Congratulations!",
        description=f"Congratulations, {winner.mention}! You won {prize},\nopen a ticket to claim it! 🎉\n\n[Giveaway Message]({msg.jump_url})")
    em.set_footer(
        text=f"This giveaway has ended.",
        icon_url="https://cdn.discordapp.com/avatars/352793093105254402/2f8d558788a138479a797c04c7a90640.webp?size=1024")
    await msg.reply(winner.mention, embed=em)

    embed = discord.Embed(color=0x0398d8, title=f"🎉 {prize} giveaway! 🎉 [ENDED]",
                          description=f"React with 🎉 below to enter.", timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Hosted by:", value=ctx.author.mention)
    embed.add_field(name="Winner: ", value=winner.mention)
    embed.set_footer(
        text=f"This giveaway has ended.",
        icon_url="https://cdn.discordapp.com/avatars/352793093105254402/2f8d558788a138479a797c04c7a90640.webp?size=1024")
    await msg.edit(embed=embed)


@bot.command(
    name="rr",
    description="Rerolls a giveaway"
)
@commands.has_permissions(manage_guild=True)
async def rr(ctx, channel: discord.TextChannel, id):
    try:
        new_msg = await channel.fetch_message(id)
    except:
        await ctx.respond("The id was entered incorrectly.")
        return

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))

    winner = random.choice(users)

    em = discord.Embed(
        color=0x0398d8, title="Congratulations!",
        description=f"Congratulations, {winner.mention}! You won by this [Giveaway]({new_msg.jump_url}) by getting rerolled,\nopen a ticket to claim it! 🎉")
    em.set_footer(
        text=f"This giveaway has been rerolled.",
        icon_url="https://cdn.discordapp.com/avatars/352793093105254402/2f8d558788a138479a797c04c7a90640.webp?size=1024")
    await ctx.respond(winner.mention, embed=em)


@bot.command(
    name="help",
    description="Sends a help embed"
)
async def help(ctx):
    em = discord.Embed(color=0x0398d8)
    em.set_author(name="noemt's giveaways | Prefix = /")
    em.add_field(name="Utility",
                 value=f"`start` - starts a giveaway (answer the following questions)\n`rr` `<Channel ID>` `<Message ID>` - rerolls a giveaway",
                 inline=False)
    em.add_field(
        name="Other",
        value=f"To invite the bot, click [here!](https://discord.com/api/oauth2/authorize?client_id=932686267366383616&permissions=543313885249&scope=bot%20applications.commands)\nYou need `Manage Server` permissions to manage Giveaways!",
        inline=False)
    await ctx.respond(embed=em)


@bot.command(
    name="vote",
    description="Vote for the bot! <3"
)
async def vote(ctx):
    em = discord.Embed(color=0x0398d8, title="Vote!",
                       description="To vote for this bot, click [here!](https://discordbotlist.com/bots/noemts-giveaways/upvote)")
    em.set_footer(
        text=f"Voting is appreciated, thank you! ",
        icon_url="https://cdn.discordapp.com/avatars/352793093105254402/2f8d558788a138479a797c04c7a90640.webp?size=1024")
    await ctx.respond(embed=em)


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=f"{str(len(bot.guilds))} guilds, /help"))


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(color=0x0398d8, title="Something's wrong..",
                           description=f"This command is on cooldown! Try again in {round(error.retry_after)} seconds.")
        em.set_footer(
            text=f"Don't spam commands.",
            icon_url="https://cdn.discordapp.com/avatars/352793093105254402/2f8d558788a138479a797c04c7a90640.webp?size=1024")
        await ctx.respond(embed=em, ephemeral=True)


for dir_name in ["commands"]:
    for file in os.listdir(dir_name):
        if file.endswith(".py"):
            bot.load_extension(f"{dir_name}.{file}".replace('.py', ''))


bot.run(os.getenv("TOKEN"))
""" create a .env file in the following format:
TOKEN=<your bot token>

OR:
bot.run("<your bot token>")
""" 
