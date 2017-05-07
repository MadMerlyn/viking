import discord
from discord.ext import commands
import math
import operator
import random
import json
import requests
from functools import reduce


### Bot Prefix ###
# You must use an asterisk * before any command to use Viking.

Viking = commands.Bot(command_prefix='*')

### Successfully Connected ###
# When Viking has connected to your server, it will output it to the command prompt.

@Viking.event
async def on_ready():
    print("\nUsername: %s " % Viking.user.name)
    print("User ID: %s " % Viking.user.id)

@Viking.event
async def on_message(message):
    if message.author == Viking.user:
        return

    ### Guessing Game ###
    # Viking will play the guessing game.
    # eg. *guess

    if message.content.startswith('*guess'):
        await Viking.send_message(message.channel, 'Lets play a game! You have to guess a number between 1 to 10.')
        guess = await Viking.wait_for_message(author=message.author)

        answer = random.randint(1, 10)
        counter = 1

        while True:
            try:
                while int(guess.content) != answer:
                    counter += 1
                    if int(guess.content) > answer:
                        await Viking.send_message(message.channel, 'Your guess is too high! Try again.')
                        guess = await Viking.wait_for_message(author=message.author)
                    else:
                        await Viking.send_message(message.channel, 'Your guess is too low! Try again.')
                        guess = await Viking.wait_for_message(author=message.author)
                else:
                    if counter <= 1:
                        await Viking.send_message(message.channel, 'Congratulations! You got it on your first try!')
                        break
                    else:
                        await Viking.send_message(message.channel, 'Congratulations! It took you **%d** tries to guess the correct answer.' % counter)
                        break
            except ValueError:
                    await Viking.send_message(message.channel, 'Please enter a number.')
                    guess = await Viking.wait_for_message(author=message.author)
                    pass

    ### Summon Bot ###
    # Viking will join the voice channel you're connected to.
    # eg. *summon

    if message.content.startswith('*summon'):
        await Viking.join_voice_channel(message.author.voice_channel)

    await Viking.process_commands(message)

### Command List ###
# Viking will list all available commands in the text channel.
# eg. *commands

@Viking.command()
async def commands(*args):
    return await Viking.say("```*hello \n*summon \n*forecast \n*guess \n*eightball \n*quotes \n*facts \n*coinflip \n*repeat \n*clear \n*add \n*subtract \n*multiply \n*divide \n*exponent \n*squareroot```")

### Hello ###
# Viking will greet you with different variations of hello.
# eg. *hello

@Viking.command()
async def hello(*greetings : str):
    greetings = ["Hey!", "Hello!", "Hi!", "Hallo!", "Bonjour!", "Hola!"]
    await Viking.say(random.choice(greetings))

### Calculator ###
# Viking supports the following operators: +, -, *, /, ^
# (add, subtract, multiply, divide, exponent)
# you can also use words like "6 minus 3"
"""word translation not yet implemented"""
# however the values must always be numerical

@Viking.command()
async def calc(*args):
    try:
        args = list(args)
        original = ''.join(args)
        args = [x.replace('^', '**') for x in args]
        problem = ''.join(args)
        answer = eval(problem, {"__builtins__": None}, {})
    except:
        await Viking.say("I don't understand that non-sense")
        return
    await Viking.say(original+' = '+str(answer))

@Viking.command()
async def squareroot(x : int):
    await Viking.say(math.sqrt(x))

### Eightball ###
# Viking will give you an eightball response to any question you ask.
# eg. *eightball Are you the best bot?

@Viking.command()
async def eightball(str, *choices : str):
    choices = ["Absolutely!", "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes, definitely.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Hell yes.", "Ask me again later.", "I better not tell.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
    await Viking.say(random.choice(choices))

### Facts ###
# Viking will provide you with a random fact.
# eg. *facts

@Viking.command()
async def facts(*facts : str):
    facts = ["Banging your head against a wall burns 150 calories an hour.", "When hippos are upset, their sweat turns red.", "A flock of crows is known as a murder.", "The average woman uses her height in lipstick every 5 years.", "Human saliva has a boiling point three times that of regular water.", "During your lifetime, you will produce enough saliva to fill two swimming pools.", "An eagle can kill a young deer and fly away with it.", "King Henry VIII slept with a gigantic axe beside him."]
    await Viking.say(random.choice(facts))

### Quotes ###
# Viking will provide you with a random quotation.
# eg. *quotes

@Viking.command()
async def quotes(*quotes : str):
    quotes = ["“You can do anything, but not everything.” - David Allen", "“The richest man is not he who has the most, but he who needs the least” - Unknown Author", "“You miss 100 percent of the shows you never take.” - Wayne Gretzky", "“Courage is not the absence of fear, but rather the judgement that something else is more important than fear.” - Ambrose Redmoon", "“You must be the change you wish to see in the world” - Gandhi", "“When hungry, eat your rice; when tired, close your eyes. Fools may laugh at me, but wise men will know what I mean.” - Lin-Chi",]
    await Viking.say(random.choice(quotes))

### Coinflip ###
# Viking will randomly choose between "heads" or "tails".
# eg. *coinflip

@Viking.command()
async def coinflip(*coinflip : str):
    coinflip = ["Heads!", "Tails!"]
    await Viking.say(random.choice(coinflip))

### Repeat ###
# Viking will repeat a sentence a certain amount of times.
# eg. *repeat 5 Viking is cool

@Viking.command()
async def repeat(times : int, *content : str):
    content = ' '.join(content)
    for i in range(times):
        await Viking.say(content)

### Forecast ###
# Viking will tell you the forecast for a location.
# eg. *forecast Edmonton AB

@Viking.command()
async def forecast(*args):
    args = ' '.join(args)
    url = "http://api.openweathermap.org/data/2.5/weather?q="+args+"&units=metric&APPID=b709f57700e58b0b221c8ee2287ee098"
    data = requests.get(url)
    read = data.json()
    location = "**Location:** {}".format(read['name'])
    temperature = "**Temperature:** {}".format(read['main']['temp']) + u' \N{DEGREE SIGN}C'
    humidity = "**Humidity:** {}".format(read['main']['humidity']) + "%"
    windspeed = "**Wind Speed:** {}".format(read['wind']['speed']) + " m/s"
    description = "**Description:** {}".format(read['weather'][0]['description'])
    await Viking.say(location)
    await Viking.say(temperature)
    await Viking.say(humidity)
    await Viking.say(windspeed)
    await Viking.say(description)

### Clear Messages ###
# Viking will clear a certain amount of messages from a text channel. (
# eg. *clear 100

@Viking.command(pass_context=True)
async def clear(ctx, messagelimit : int):
    deleted = await Viking.purge_from(ctx.message.channel, limit=messagelimit)
    await Viking.say("I have cleared **{}** messages.".format(len(deleted)))

### Bot Status ###
# Viking will change its status in Discord.
# eg. *status Discord

@Viking.command()
async def status(*args):
    args = ' '.join(args)
    await Viking.change_presence(game = discord.Game(name="%s" % args))

### An empty command for the guessing game. ###
# This will prevent an error from being displayed in the command prompt.

@Viking.command()
async def guess():
    print("")

### An empty command to summon the bot into your channel. ###
# This will prevent an error from being displayed in the command prompt.

@Viking.command()
async def summon():
    print("")

### Authenticate ###
# Go to: https://discordapp.com/developers/applications/me
# Login
# Select "New App"
# Name your bot
# Press "Create Application"
# Click on "Create a Bot User", then "Yes, do it!"
# Look for "Token", and then "click to reveal".
# Add the token below:

Viking.run('YOUR_TOKEN_HERE')

### Add the bot to your server ###
# Go to: https://discordapp.com/developers/applications/me
# Select the bot you have created
# Copy the Client ID, and paste it into the URL below (where it says "YOUR_CLIENT_ID_HERE"):
# Copy and paste the following into your browser: https://discordapp.com/oauth2/authorize?&client_id=YOUR_CLIENT_ID_HERE&scope=bot&permissions=0
