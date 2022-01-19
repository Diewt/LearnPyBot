import os
import discord 
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
import pytz
import database

# Grabbing Evironment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Initial Database Creation
database.createTable()

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

# Command to print out time in timezone
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

# Command to Register User into Database
@client.command()
async def register(message):
    print(message.author.id)
    if database.registerUser(message.author.id):
        await message.channel.send('You are already registered')
    else:
        await message.channel.send('You are successfully Registered')

client.run(TOKEN)