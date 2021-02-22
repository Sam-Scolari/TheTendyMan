import discord
from discord.ext.commands import Bot
from Crawlers import reddit, yahoo
import json
import credentials

bot = Bot(command_prefix="$")

@bot.event
async def on_message(msg):
    if (len(msg.content) > 1 and msg.content[0] == '$' and msg.author.id != bot.user.id):
        data = json.loads(yahoo.fetch(msg.content[1:]))

        business_name = data['business_name']
        stock_price = data['stock_price']
        last_close = data['last_close']
        price_change = str(float(stock_price) - float(last_close))[:5]
        percent_change = str((float(price_change) / float(last_close))* 100)[:5] 
        image = data['image']

        embed = discord.Embed(title=f'{business_name}', color=discord.Color.red() if float(price_change) < 0 else discord.Color.green())
        embed.add_field(name='**Quote**', value=f'Price: ${stock_price}\nChange: {price_change[0]}${price_change[1:]} ({percent_change}%)')
        embed.set_thumbnail(url=f'{image}')
      
        await msg.channel.send(embed=embed)
        # await msg.channel.send(file=discord.File('image0.png'))

@bot.command()
async def price(ctx, arg):
    await ctx.send(yahoo.fetch())

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = 'The Stock Market'))
    print('Bot Ready!')


bot.run(credentials.bot_token)