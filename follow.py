import discord
from discord.ext import tasks, commands

from datetime import datetime, timezone
from Crawlers import marketwatch
import json


class Follow(commands.Cog):


    def __init__(self, bot):
        self.bot = bot

        self.refresh_rate = 15
        self.followed_stocks_channel = None #updated in on_ready



    def add_to_followed(self, stock: str):
        '''
        Adds newly-followed stocks to the
        followed-stocks text file.
        '''
        
        with open('followed-stocks.txt', 'a') as f:
            f.append(f'{stock}\n')



    def remove_from_followed(self, stock: str) -> bool:
        '''
        Removes unfollowed stocks from the
        followed-stocks text file.

        Returns True if stock was found in
        the currently followed stocks and
        successfully removed, False if not.
        '''

        found_in_list = False
        
        with open('followed-stocks.txt', "r") as f:
            lines = f.readlines()

        with open('followed-stocks.txt', 'w') as f:
            for line in lines:
                if line.strip('\n') != 'stock':
                    f.write(line)

                else:
                    found_in_list = True

        return found_in_list



    def get_followed_stocks(self) -> list:
        '''
        Returns a list of all of the
        currently followed stocks.
        '''
        
        with open('followed-stocks.txt', 'r') as f:
            lines = f.readlines()

        return [line.strip('\n') for line in lines]



    def retrieve_necessary_stock_info(self) -> dict:
        '''
        Returns a dictionary containing the
        necessary info related to each ticker,
        currently comprising of each ticker's
        current price, their $ change today,
        and their % change today.
        '''
        
        data_dict = {}

        for ticker in self.get_followed_stocks():
            data = json.loads(marketwatch.get_quote(ticker))

            data_dict[ticker]['current_price'] = data['price']
            data_dict[ticker]['price_change'] = data['price-change']
            data_dict[ticker]['percent_change'] = percent_change = data['percent-change']

        return data_dict



    def get_date_info(self) -> tuple:
        '''
        Returns tuple of weekday in 0-6
        format and CST time in 24hr format.
        '''

        date_obj = datetime.now()

        day = date_obj.weekday()
        current_hour = date_obj.hour
        
        return (day, current_hour)



    def construct_embed(self) -> discord.Embed:
        '''
        Constructs embed to be used to
        display data of all followed
        stocks.
        '''
        
        stock_data = self.retrieve_necessary_stock_info()

        price_change_list = []
        percent_change_list = []

        for ticker in stock_data.keys():
            price_change_list.append(stock_data[ticker]['price_change'])
            percent_change_list.append(stock_data[ticker]['percent_change'])

        ticker_list = '\n'.join(self.get_followed_stocks())
        price_change_list = '\n'.join(price_change_list)
        percent_change_list = '\n'.join(percent_change_list)


        embed = discord.Embed(title='Followed Stocks', colour=0x00ff04)
        embed.add_field(name='Tickers', value=ticker_list, inline=True)
        embed.add_field(name='Price Change', value=price_change_list, inline=True)
        embed.add_field(name='Percent Change', value=percent_change_list, inline=True)

        return embed



    def send_initial_msg(self):
        '''
        Called when either there are no
        messages in the #followed-stocks
        channel, or a new message should
        be sent in the channel at the start
        of the new trading day.
        '''

        embed = self.construct_embed()
        
        self.followed_stocks_channel.send(embed=embed)



    def update_last_message(self, message):
        '''
        Updates the previous message sent
        in #followed-stocks with the most
        recent information collected.

        Takes Context object of the last
        message the bot sent in the
        #followed-stocks channel as message.
        '''
        
        embed = self.construct_embed()

        previous_message = self.followed_stocks_channel.history(limit=1)
        previous_message[0].edit(embed=embed)



    @commands.Cog.listener()
    async def on_ready(self):
        '''
        Retrieves the channel object for the
        #followed-stocks channel, as 
        bot.get_channel() does not work when
        used in __init__().
        '''

        self.followed_stocks_channel = self.bot.get_channel(814686739952041994)

        self.update_stocks.start() #begin update_stocks task loop



    @tasks.loop(minutes=self.refresh_rate)
    async def update_stocks(self):
        '''
        Updates the message with the most
        recent data on each followed stock.
        '''
        
        if self.followed_stocks_channel is None:
            print('#followed-stocks channel has not been properly retrieved.')
            return

        #only need last message
        previous_message = self.followed_stocks_channel.history(limit=1)
        day, current_hour = self.get_date_info()


        #if not currently in trading hours
        if day in [5, 6] or current_hour not in range(8, 17): 
            return

        #currently in trading hours
        else:
            #no messages in #followed-stocks yet
            if len(previous_message) == 0:
                self.send_initial_msg()
            
            #check if last message sent was from yesterday to know if new one needs to be sent
            elif previous_message[0].created_at.weekday() != day:
                self.send_initial_msg()

            #last message in #followed-stocks is from today and needs to be edited
            else:
                self.update_last_message(previous_message[0])



    @commands.command(aliases=['rt'])
    async def refresh_time(self, ctx, time: int):
        '''
        Sets the amount of time elapsed between
        data updates, in minutes.
        '''
        
        self.refresh_rate = time

        await ctx.send(f'Successfully set the refresh time to {time} minutes.')


    @commands.command()
    async def follow(self, ctx, stock: str):
        '''
        Stocks that are followed will have their
        current price, $ change and % change updated
        throughout each trading day via a message
        in the #followed-stocks channel.
        '''
        
        self.add_to_followed(stock)

        await ctx.send(f'{stock} was successfully added to followed stocks.')

    @commands.command()
    async def unfollow(self, ctx, stock: str):
        '''
        Stocks that are unfollowed will be removed
        from their place in the #followed-stocks
        channel, and will no longer be followed.
        '''
        
        success = self.remove_from_followed(stock)

        if success:
            await ctx.send(f'{stock} will no longer be followed.')

        else:
            await ctx.send(f'{stock} was not among the currently followed stocks.')



def setup(bot):
    bot.add_cog(Follow(bot))