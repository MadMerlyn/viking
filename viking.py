import discord
from discord.ext import commands
import asyncio
import pyowm
from math import sqrt
import random
from random import randint

### Bot Prefix ###
# You must use an asterisk * before any command to use Viking.

Viking = commands.Bot(command_prefix='*')

@Viking.event
async def on_ready():
    """ ### Successfully Connected ###
    When Viking has connected to your server,
    it will output it to the command prompt."""

    print('\nUsername: %s ' % Viking.user.name)
    print('User ID: %s ' % Viking.user.id)

@Viking.command()
async def hello(*greetings : str):
    """ ### Hello ###
    Viking will greet you with different variations of hello.
    eg. *hello"""
    greetings = ['Hey!', 'Hello!', 'Hi!', 'Hallo!', 'Bonjour!', 'Hola!']
    await Viking.say(random.choice(greetings))

@Viking.command()
async def calc(*args):
    """### Calculator ###
    Viking supports +, -, *, /, %, and sqrt()"""

    try:
        args = list(args)
        original = ''.join(args)
        original = original.replace('*', '\*')
        problem = ''.join(args)
        problem = problem.replace('^', '**')
        answer = eval(problem, {'__builtins__': None}, {'sqrt':sqrt})
    except:
        await Viking.say('I\'m sorry. I don\'t understand that.')
        return
    await Viking.say(original+' = '+str(answer))

@Viking.command()
async def eightball(str, *choices : str):
    """### Eightball ###
    Viking will give you an eightball response to any question you ask.
    eg. *eightball Are you the best bot?"""

    choices = ['Absolutely!', 'It is certain.', 'It is decidedly so.',
               'Without a doubt.', 'Yes, definitely.', 'As I see it, yes.',
               'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
               'Hell yes.', 'Ask me again later.', 'I better not tell.',
               'Don\'t count on it.', 'My reply is no.', 'My sources say no.',
               'Outlook not so good.', 'Very doubtful.']
    await Viking.say(random.choice(choices))

@Viking.command()
async def facts(*facts : str):
    """### Facts ###
    Viking will provide you with a random fact.
    eg. *facts"""

    facts = [
    'Banging your head against a wall burns 150 calories an hour.',
    'When hippos are upset, their sweat turns red.',
    'A flock of crows is known as a murder.',
    'The average woman uses her height in lipstick every 5 years.',
    'Human saliva has a boiling point three times that of regular water.',
    'During your lifetime, you will produce enough saliva to fill two\
    swimming pools.',
    'An eagle can kill a young deer and fly away with it.',
    'King Henry VIII slept with a gigantic axe beside him.']
    await Viking.say(random.choice(facts))

@Viking.command()
async def quotes(*quotes : str):
    """### Quotes ###
    Viking will provide you with a random quotation.
    eg. *quotes"""

    quotes = [
    '“You can do anything, but not everything.” - David Allen',
    '“The richest man is not he who has the most, but he who needsthe least”\
    - Unknown Author',
    '“You miss 100 percent of the shows you never take.” -Wayne Gretzky',
    '“Courage is not the absence of fear, but rather the judgement\
    that something else is more important than fear.” -Ambrose Redmoon',
    '“You must be the change you wish to see in the world” - Gandhi',
    '“When hungry, eat your rice; when tired, close your eyes. Fools\
    may laugh at me, but wise men will know what I mean.” - Lin-Chi',]
    await Viking.say(random.choice(quotes))

@Viking.command()
async def coinflip(*coinflip : str):
    """### Coinflip ###
    Viking will randomly choose between 'heads' or 'tails'.
    eg. *coinflip"""

    coinflip = ['Heads!', 'Tails!']
    await Viking.say(random.choice(coinflip))

@Viking.command()
async def repeat(times : int, *content : str):
    """### Repeat ###
    Viking will repeat a sentence a certain amount of times.
    eg. *repeat 5 Viking is cool"""

    content = ' '.join(content)
    for i in range(times):
        await Viking.say(content)

@Viking.command()
async def forecast(*name : str):
    """### Forecast ###
    Viking will tell you the forecast for a location.
    eg. *forecast Edmonton AB"""

    name = ' '.join(name)
    owm = pyowm.OWM('YOUR_TOKEN_HERE')

    observation = await Viking.loop.run_in_executor(None, partial(owm.weather_at_place, name))
    weather = await Viking.loop.run_in_executor(None, partial(observation.get_weather))
    location = await Viking.loop.run_in_executor(None, partial(observation.get_location))
    get_temperature = await Viking.loop.run_in_executor(None, partial(weather.get_temperature, unit='celsius'))
    get_wind = await Viking.loop.run_in_executor(None, partial(weather.get_wind))

    location = "**Location:** {}".format(location.get_name())
    temperature = "**Temperature:** {}".format(get_temperature['temp']) + u' \N{DEGREE SIGN}C'
    humidity = "**Humidity:** {}".format(weather.get_humidity()) + "%"
    windspeed = "**Wind Speed:** {}".format(get_wind['speed']) + " m/s"
    status = "**Description:** {}".format(weather.get_detailed_status())

    await Viking.say(location)
    await Viking.say(temperature)
    await Viking.say(humidity)
    await Viking.say(windspeed)
    await Viking.say(status)

@Viking.command(pass_context=True)
async def clear(ctx, messagelimit : int):
    """### Clear Messages ###
    Viking will clear a certain amount of messages from a text channel. (
    eg. *clear 100"""

    deleted = await Viking.purge_from(ctx.message.channel, limit=messagelimit)
    await Viking.say('I have cleared **{}** messages.'.format(len(deleted)))

@Viking.command()
async def status(*args):
    """### Bot Status ###
    Viking will change its status in Discord.
    eg. *status Discord"""

    args = ' '.join(args)
    await Viking.change_presence(game = discord.Game(name='%s' % args))

@Viking.command(pass_context=True)
async def guess(ctx):
    """### Guessing Game ###
    Viking will play the guessing game.
    eg. *guess"""

    await Viking.say('Lets play a game! You have to guess a number between\
                     1 and 10.')
    guess = await Viking.wait_for_message(author=ctx.message.author)

    answer = random.randint(1, 10)
    counter = 1

    while True:
        try:
            while int(guess.content) != answer:
                counter += 1
                if int(guess.content) > answer:
                    await Viking.say('Your guess is too high! Try again.')
                    guess = await Viking.wait_for_message(
                            author=ctx.message.author)
                else:
                    await Viking.say('Your guess is too low! Try again.')
                    guess = await Viking.wait_for_message(
                            author=ctx.message.author)
            else:
                if counter <= 1:
                    await Viking.say('Congratulations!\
                                     You got it on your first try!')
                    break
                else:
                    await Viking.say('Congratulations! It took you\
                    **%d** tries to guess the correct answer.' % counter)
                    break
        except ValueError:
                await Viking.say('Please enter a number.')
                guess = await Viking.wait_for_message(
                        author=ctx.message.author)
                pass

@Viking.command(pass_context=True)
async def summon(ctx):
    """### Summon Bot ###
    Viking will join the voice channel you're connected to.
    eg. *summon"""

    await Viking.join_voice_channel(ctx.message.author.voice_channel)

### Authenticate ###
# Go to: https://discordapp.com/developers/applications/me
# Login
# Select 'New App'
# Name your bot
# Press 'Create Application'
# Click on 'Create a Bot User', then 'Yes, do it!'
# Look for 'Token', and then 'click to reveal'.
# Add the token below:

Viking.run('YOUR_TOKEN_HERE')

### Add the bot to your server ###
# Go to: https://discordapp.com/developers/applications/me
# Select the bot you have created
# Copy the Client ID, and paste it into the URL below
# (where it says 'YOUR_CLIENT_ID_HERE'):
# Copy and paste the following into your browser:
# https://discordapp.com/oauth2/authorize?&client_id=YOUR_CLIENT_ID_HERE&scope=bot&permissions=0
