# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
import discord
import time
import datetime
import sqlite3
from discord import Game
from discord.ext.commands import Bot


BOT_PREFIX = ("*", "?", "!")
TOKEN = "NDEzMDk5NTY5NTM5MzE3NzY5.DtXrdA.cBr5R_Szbg7vAwBCZljOkvxL26k"  # Get at discordapp.com/developers/applications/me

# Create bot
client = Bot(command_prefix=BOT_PREFIX)
# Create a database in RAM
'''db = sqlite3.connect(':memory:')'''
# Creates or opens a file called mydb with a SQLite3 DB
db = sqlite3.connect('data/memberdb')
# Cursor for database management
cursor = db.cursor()
# Creating Table for member data
cursor.execute('''CREATE TABLE IF NOT EXISTS members(id INTEGER PRIMARY KEY, name TEXT, class TEXT, level TEXT, xp TEXT)''')
db.commit()

'''Admin Commands'''
# Kick Command
@client.command(name='kick',
                description="Kicks a member from the server.",
                brief="Server Kick.",
                pass_context = True)
async def kick(ctx, user_name: discord.User):
    await client.kick(user_name)

# Ban Command
@client.command(name='ban',
                description="Bans a member from the server.",
                brief="Unban member.",
                pass_context = True)
async def ban(ctx, user_name: discord.User, message_days):
    await client.ban(user_name, message_days)

# Nickname Command
@client.command(name='nick',
                description="Nicknames a member in the server (Leave blank to clear nickname).",
                brief="Nickname member (Leave blank to clear nickname).",
                pass_context = True)
async def nick(ctx, member: discord.User, nick_name=None):
    await client.change_nickname(member, nick_name)

# Ban List Command
@client.command(name='banlist',
                description="Gets the currently banned users of server.",
                brief="Gets bans of server.",
                pass_context = True)
async def banlist(ctx):
    server = ctx.message.server
    ban_list = await client.get_bans(server)
    await client.say("Ban list:\n{}".format("\n".join([user.name for user in ban_list])))



# Clear Chat Command
@client.command(name='clear',
                description='Clear comments from a certain chat channel that are not older than 14 days.',
                brief='Clear chat channel messages under 14 days old.',
                pass_context = True)
async def clear(ctx, number):
    mgs = [] #Empty list to put all the messages in the log
    number = int(number) #Converting the amount of messages to delete to an integer
    async for x in client.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await client.delete_messages(mgs)

'''
@client.command(name='promote',
                description='Promotes a user up the role hierarchy.',
                brief='Promote users role.',
                pass_context = True)
async def promote():
'''

'''Commands'''
# 8Ball Command
@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

# Rock Paper Scissors Lizard Spock Command
@client.command(name='throw',
                description="Throw a gesture towards the bot to play rock paper scissors lizard spock.",
                brief="Play rock paper scissors lizard spock.",
                pass_context=True)
async def throw(player):
    choices = ['rock', 'paper', 'scissors', 'lizard', 'spock']
    computer = choices[random.randrange(len(choices))]
    if ((player == 'rock') and (computer == 'rock')):
        await client.say("Tie")
    elif ((player == 'rock') and (computer == 'paper')):
        await client.say("You lose: paper covers rock")
    elif ((player == 'rock') and (computer == 'scissors')):
        await client.say("You win: rock crushes scissors")
    elif ((player == 'rock') and (computer == 'lizard')):
        await client.say("You win: rock crushes lizard")
    elif ((player == 'rock') and (computer == 'spock')):
        await client.say("You lose: spock vaporizes rock")
    elif ((player == 'paper') and (computer == 'rock')):
        await client.say("You win: paper covers rock")
    elif ((player == 'paper') and (computer == 'paper')):
        await client.say("Tie")
    elif ((player == 'paper') and (computer == 'scissors')):
        await client.say("You lose: scissors cuts paper")
    elif ((player == 'paper') and (computer == 'lizard')):
        await client.say("You lose: lizard eats paper")
    elif ((player == 'paper') and (computer == 'spock')):
        await client.say("You win: paper disproves spock")
    elif ((player == 'scissors') and (computer == 'rock')):
        await client.say("You lose: rock crushes scissors")
    elif ((player == 'scissors') and (computer == 'paper')):
        await client.say("You win: scissors cuts paper")
    elif ((player == 'scissors') and (computer == 'scissors')):
        await client.say("Tie")
    elif ((player == 'scissors') and (computer == 'lizard')):
        await client.say("You win: scissors decapitates lizard")
    elif ((player == 'scissors') and (computer == 'spock')):
        await client.say("You lose: spock smashes scissors")
    elif ((player == 'lizard') and (computer == 'rock')):
        await client.say("You win: rock crushes lizard")
    elif ((player == 'lizard') and (computer == 'paper')):
        await client.say("You win: lizard eats paper")
    elif ((player == 'lizard') and (computer == 'scissors')):
        await client.say("You lose: scissors decapitates lizard")
    elif ((player == 'lizard') and (computer == 'lizard')):
        await client.say("Tie")
    elif ((player == 'lizard') and (computer == 'spock')):
        await client.say("You win: lizard poisons spock")
    elif ((player == 'spock') and (computer == 'rock')):
        await client.say("You win: spock vaporizes rock")
    elif ((player == 'spock') and (computer == 'paper')):
        await client.say("You lose: paper disproves spock")
    elif ((player == 'spock') and (computer == 'scissors')):
        await client.say("You win: spock smashes scissors")
    elif ((player == 'spock') and (computer == 'lizard')):
        await client.say("You lose: lizard poisons spock")
    elif ((player == 'spock') and (computer == 'spock')):
        await client.say("Tie")

#Coin Flip Command
@client.command(name='flip',
                description="Flip a coin and see if its heads or tails.",
                brief="Flip a coin.",
                pass_context=True)
async def flip():
    randnum = random.randint(1,3)
    if randnum == 0:
        await client.say("Heads")
    else:
        await client.say("Tails")

# Square Number Command
@client.command(name='square',
                description="Find out what the square of a number is.",
                brief="Square a number.",
                pass_context=True)
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))

#Bitcoin Price Command
@client.command(name='bitcoin',
                description="Gives a global current price of the current BTC values.",
                brief="Show current bitcoin price",
                pass_context=True)
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

@client.command(brief="Show member info")
async def stat(ctx, member: discord.User):
    # Fetch user information
    cursor.execute('''SELECT name, class, level, xp FROM members WHERE id=?''', (member,))
    member_name = cursor.fetchone()
    member_class = cursor.fetchone()
    member_level = cursor.fetchone()
    member_xp = cursor.fetchone()
    await client.say("NAME: " + str(member_name)  + "\n CLASS: " + str(member_class) + "\n LEVEL: " + str(member_level) + "\n XP: " + str(member_xp))

'''Bot logging and other'''
@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Destroy All Humans! "))
    print("Logged in as " + client.user.name)

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

client.loop.create_task(list_servers())
client.run(TOKEN)