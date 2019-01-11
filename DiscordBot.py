# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
import discord
import time
import datetime
import asyncio
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
cursor.execute('''CREATE TABLE IF NOT EXISTS members(id INTEGER PRIMARY KEY, name TEXT UNIQUE, race TEXT, class TEXT, level TEXT, xp TEXT)''')
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
                pass_context=False)
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
                pass_context=False)
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
                pass_context=False)
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

# Rules Command
@client.command(name='rules',
                description='Display the rules of the RPG game.',
                brief='RPG rules.',
                pass_context = False)
async def rules():
    await client.say("Rules:\n" + "Races: Human, Elf, Dwarf, Halfling, Gnome, Half-Orc\n" + "Classes: Fighter, Wizard, Cleric, Rogue, Ranger\n" + "Factions: The Harpers, "
                    + "The Order of the Gauntlet, The Emerald Enclave, The Lords' Alliance, The Zhentarim\n")

# More information command
@client.command(name='info',
                description='Display the rules of the RPG game.',
                brief='RPG rules.',
                pass_context = True)
async def info(ctx, word):
    word.lower()
    if (word == "human") or (word == "Human"):
        await client.say("Whatever drives them, humans are the innovators, the achievers, and the pioneers of the worlds.")
    elif (word == "elf") or (word == "Elf"):
        await client.say("Elves are a magical people of otherworldly grace, living in the world but not entirely part of it.")
    elif (word == "dwarf") or (word == "Dwarf"):
        await client.say("Dwarves are solid and enduring like the mountains they love, weathering the passage of centuries with stoic endurance and little change.")
    elif (word == "halfling") or (word == "Halfling"):
        await client.say("The comforts of home are the goals of most halflings’ lives: a place to settle in peace and quiet, far from marauding monsters and clashing armies.")
    elif (word == "gnome") or (word == "Gnome"):
        await client.say("Gnomes take delight in life, enjoying every moment of invention, exploration, investigation, creation, and play.")
    elif (word == "half-orc") or (word == "Half-Orc"):
        await client.say("Half-orcs are not evil by nature, but evil does lurk within them, whether they embrace it or rebel against it.")
    elif (word == "fighter") or (word == "Fighter"):
        await client.say("Questing knights, conquering overlords, royal champions, elite foot soldiers, hardened mercenaries, and bandit kings—as fighters, they all share an unparalleled mastery with weapons and armor, and a thorough knowledge of the skills of combat.")
    elif (word == "wizard") or (word == "Wizard"):
        await client.say("Drawing on the subtle weave of magic that permeates the cosmos, wizards cast spells of explosive fire, arcing lightning, subtle deception, and brute-force mind control.")
    elif (word == "cleric") or (word == "Cleric"):
        await client.say("Clerics are intermediaries between the mortal world and the distant planes of the gods. As varied as the gods they serve, they strive to embody the handiwork of their deities.")
    elif (word == "rogue") or (word == "Rouge"):
        await client.say("Rogues rely on skill, stealth, and their foes’ vulnerabilities to get the upper hand in any situation. They have a knack for finding the solution to just about any problem, bringing resourcefulness and versatility to their adventuring parties.")
    elif (word == "ranger") or (word == "Ranger"):
        await client.say("Far from the bustle of cities and towns, amid the dense-packed trees of trackless forests and across wide and empty plains, rangers keep their unending watch.")
    elif (word == "harpers") or (word == "Harpers"):
        await client.say("An old organization that has risen, been shattered, and risen again several times. Its longevity and resilience are largely due to its decentralized, grassroots, secretive nature, and the near-autonomy of many of its members.")
    elif (word == "gauntlet") or (word == "Gauntlet"):
        await client.say("Many paladins and clerics of Tyr, Helm, Torm, and Hoar have joined this new organization, seeing it as—finally—a way of making common cause against the evils abroad in the world.")
    elif (word == "enclave") or (word == "Enclave"):
        await client.say("A far-ranging group that opposes threats to the natural world and helps others survive the many perils of the wild. Members of the Emerald Enclave are spread far and wide, and usually operate in isolation.")
    elif (word == "alliance") or (word == "Alliance"):
        await client.say("A coalition of rulers from cities across Faerûn, who collectively agree that some solidarity is needed to keep evil at bay. The rulers of Waterdeep, Silverymoon, Neverwinter, and other free cities in the region dominate the Alliance.")
    elif (word == "zhentarim") or (word == "Zhentarim"):
        await client.say("The Zhentarim seeks to become omnipresent and inescapable, more wealthy and powerful, and most importantly, untouchable. Everyone should fear to cross them.")
    else:
        await client.say("Not a Race/Class/Faction please try: !info <human/elf/dwarf/halfling/gnome/half-orc/fighter/wizard/cleric/rogue/ranger/harpers/gauntlet/enclave/alliance/zhentarim>")

# New game command
@client.command(name='newgame',
                description='Create a new RPG game with no members.',
                brief='New RPG game.',
                pass_context = False)
async def newgame():
    # Delete existing table
    cursor.execute('''DROP TABLE members''')
    db.commit()
    # Create new table
    cursor.execute('''CREATE TABLE IF NOT EXISTS members(id INTEGER PRIMARY KEY, name TEXT, race TEXT, class TEXT, level TEXT, xp TEXT)''')
    db.commit()

# Join game command
@client.command(name='join',
                description='Join the RPG game that is being played',
                brief='Join RPG',
                pass_context = True)
async def join(ctx, member_race, member_class):
    member_name = ctx.message.author.name
    member_level = 1
    member_xp = 0
    # Insert user into database
    cursor.execute('''INSERT OR REPLACE INTO members(name, race, class, level, xp)VALUES(?,?,?,?,?)''', (str(member_name), str(member_race), str(member_class), str(member_level), str(member_xp)))
    await client.say("The " + str(member_race) + " " + str(member_class) + " " + str(member_name) + " has entered the world")
    db.commit()
    #await client.delete_message(message)

# List joined players command
@client.command(name='list',
                description='List members that have joined the RPG game.',
                brief='Show RPG members.',
                pass_context = False)
async def list():
    # Fetch list of user information
    cursor.execute('''SELECT name, race , class, level, xp FROM members ''')
    for row in cursor:
        await client.say("NAME: " + row[0])
        await client.say("RACE: "+ row[1])
        await client.say("CLASS: " + row[2])
        await client.say("LEVEL: " + row[3])
        await client.say("XP: " + row[4])
        await client.say("---------------------")

# Dice roll command
@client.command(name='roll',
                descsription='Roll dice',
                brief='Roll dice',
                pass_context = True)
async def roll(ctx, die_sides: int):
    if die_sides == 4:
        randnum = random.randint(1,4)
        await client.say("You rolled a " + str(randnum))
    elif die_sides == 6:
        randnum = random.randint(1,6)
        await client.say("You rolled a " + str(randnum))
    elif die_sides == 8:
        randnum = random.randint(1,8)
        await client.say("You rolled a " + str(randnum))
    elif die_sides == 10:
        randnum = random.randint(1,10)
        await client.say("You rolled a " + str(randnum))
    elif die_sides == 12:
        randnum = random.randint(1,12)
        await client.say("You rolled a " + str(randnum))
    elif die_sides == 20:
        randnum = random.randint(1,20)
        await client.say("You rolled a " + str(randnum))
    else:
        await client.say("That is not a valid die choice please use a D4, D6, D8, D10, D12, or D20 dice!")


# ***Debugging Command to delete the table***
@client.command()
async def drop_table():
    cursor.execute('''DROP TABLE members''')
    db.commit()
# ***Debugging Command to recreate the table after deletion without needing a bot restart
@client.command()
async def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS members(id INTEGER PRIMARY KEY, name TEXT, class TEXT, level TEXT, xp TEXT)''')
    db.commit()
# ***Debugging Command for users***
@client.command()
async def who(member_name: discord.User):
    await client.say(member_name)
    

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