# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("*", "?", "!")
TOKEN = "NDEzMDk5NTY5NTM5MzE3NzY5.DtXrdA.cBr5R_Szbg7vAwBCZljOkvxL26k"  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)

@client.command()
async def stats(member, days):
    member = discord.Member
    if "449706643710541824" in [role.id for role in message.author.roles]:
        await client.ban(member, days)
    else:
        await client.say("You don't have permission to use this command.")

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

@client.command()
async def rpsls(player):
    choices = ['rock', 'paper', 'scissors', 'lizard', 'spock']
    computer = choices[random.randrange(len(choices))]
    if ((player == 'rock') and (computer == 'rock')):

    elif ((player == 'rock') and (computer == 'paper')):

    elif ((player == 'rock') and (computer == 'scissors')):

    elif ((player == 'rock') and (computer == 'lizard')):

    elif ((player == 'rock') and (computer == 'spock')):

@client.command()
async def flip():
    randnum = random.randint(1,3)
    if randnum == 0:
        await client.say("Heads")
    else:
        await client.say("Tails")

@client.command()
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)


@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

client.loop.create_task(list_servers())
client.run(TOKEN)