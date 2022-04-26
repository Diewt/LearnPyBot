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

database.updateDatabase()

# Command Prefix
client = commands.Bot(command_prefix='-', intents = discord.Intents.all())

# Event Handler
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    await client.process_commands(message)
    # await message.channel.send('test')


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
        await message.channel.send('You have successfully Registered')

# Test command to update array
@client.command()
async def arrayTest(message):
    if database.isUserRegistered():
        database.updateArray(message.author.id)
    else:
        await message.channel.send('You need to register before using this command')

# Command to get list of users with x role
@client.command()
async def getUsers(message, *, roleName):
    
    # Gatherinig information such as the Server name and roles in the server
    server = message.message.guild
    roleID = server.roles[0]
    for role in server.roles:
        if roleName == role.name:
            roleID = role
            break
    else:
        await message.channel.send('Role ' + str(roleName) + ' Does not exist')
        return

    # Grabbing all the people who have that role into a list
    memberWithRole = []
    for member in server.members:
        if roleID in member.roles:
            memberWithRole.append(member.name + '#' + member.discriminator)

    # Writing the users into a text file
    userListFile = open('UserList.txt', "wb")
    for x in range(len(memberWithRole)):
        original = memberWithRole[x] + '\n'
        encode = original.encode('utf8')
        userListFile.write(encode)
    userListFile.close()

    # Inserting the text file into a discord dm have to make the file readable
    userListFile = open('UserList.txt', "rb")
    await message.author.send('These are the users with role ' + str(roleName),
    file=discord.File(userListFile ,"userList.txt")
    )
    userListFile.close()

# Command to get exp
@client.command()
async def farm(message):
    database.exp(message.author.id, 20)

client.run(TOKEN)