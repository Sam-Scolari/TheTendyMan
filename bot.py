import discord
from discord.ext import commands

import credentials

bot = commands.Bot(command_prefix="$")

extensions = ['ticker_commands','follow', 'admincommands']

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)



#this event ignores $ commands handled in on_ready, like $cciv
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error



@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = 'The Stock Market'))
    print('Bot Ready!')


bot.run(credentials.bot_token)