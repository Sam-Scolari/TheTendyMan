import discord
from discord.ext.commands import Bot
from Crawlers import reddit, yahoo, marketwatch
import json
import credentials

bot = Bot(command_prefix="$")

@bot.event
async def on_message(msg):
    if (len(msg.content) > 1 and msg.author.id != bot.user.id):
        if (msg.content[0] == '$'):
            args = msg.content[1:].split(' ')
            if len(args) == 1:
                data = json.loads(marketwatch.get_quote(msg.content[1:]))

                business_name = data['business-name']
                stock_price = data['price']
                last_close = data['last-close']
                price_change = data['price-change']
                percent_change = data['percent-change']
                image = data['image']

                embed = discord.Embed(title=f'{business_name}', color=discord.Color.red() if float(price_change) < 0 else discord.Color.green())
                embed.add_field(name='**Quote**', value=f'Price: ${stock_price}\nChange: {price_change[0]}${price_change[1:]} ({percent_change})')
                embed.set_thumbnail(url=f'{image}')
            
                await msg.channel.send(embed=embed)
                # await msg.channel.send(file=discord.File('image0.png'))

            else:
                if args[1] == 'sec':
                    sec_data = json.loads(marketwatch.get_sec_filing(args[0]))
                    quote_data = json.loads(marketwatch.get_quote(args[0]))

                    image = quote_data['image']

    
                    embed = discord.Embed(title=f'{"$"+args[0].upper() +" | Latest SEC Filing"}', color=discord.Color.dark_gold(), description=f'[View All](<https://www.marketwatch.com/investing/stock/{args[0]}/financials/secfilings>)')
                    embed.add_field(name='**Date**', value=sec_data['filing-date'][0], inline=True)
                    embed.add_field(name='**Filing**', value='[' + sec_data['document-type'][0][0] + '](<' + sec_data['document-type'][0][1] + '>)', inline=True)
                    embed.add_field(name='**Type**', value=sec_data['category'][0], inline=True)
                    embed.set_thumbnail(url=f'{image}')
                
                    await msg.channel.send(embed=embed)




@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = 'The Stock Market'))
    print('Bot Ready!')


bot.run(credentials.bot_token)