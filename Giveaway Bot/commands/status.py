import asyncio
import discord
from discord.ext import commands, tasks

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statusTask.start()

    def cog_unload(self):
        self.statusTask.cancel()
    
    @tasks.loop(minutes=2)
    async def statusTask(self):
            await self.bot.change_presence(status=discord.Status.online,
                                           activity=discord.Activity(type=discord.ActivityType.listening,
                                                                  name=f"{str(len(self.bot.guilds))} guilds, /help"))

    @statusTask.before_loop
    async def before_statusTask(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(5)

def setup(bot):
    bot.add_cog(Status(bot))
