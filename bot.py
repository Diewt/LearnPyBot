import os
import discord 
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Grabbing Evironment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Command Prefix
client = commands.Bot(command_prefix='-')

# Event Handler
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    await client.process_commands(message)
    await message.channel.send('test')



# Commands
@client.command()
async def time(message, area):
    print(area)
    try:
        timezone = pytz.timezone(area)
        date_time = datetime.now(timezone)
        print(date_time.strftime('Date:%Y/%m/%d  Time:%H:%M:%S %Z %z'))
        await message.channel.send(date_time.strftime('Date:%Y/%m/%d  Time:%H:%M:%S %Z %z'))
    except:
        print('error')
        await message.channel.send('Error: '+ area + ' is not a valid input')

        

client.run(TOKEN)