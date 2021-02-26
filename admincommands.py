import discord
from discord.ext import tasks, commands


class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def reload(self, ctx, *, module):
        '''Reloads a module.'''

        self.bot.unload_extension(module)
        self.bot.load_extension(module)

        await ctx.send(f'Successfully reloaded {module}.')


def setup(bot):
    bot.add_cog(AdminCommands(bot))