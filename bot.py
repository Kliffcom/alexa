import discord
import os
from search import search
from random import choice

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

voice = None
player = None
eyes = [':eye:', ':eye_in_speech_bubble:', ':regional_indicator_o:', ':white_circle:']
ws = [':snake:', ':cactus:', ':part_alternation_mark:', ':aries:', ':regional_indicator_w:']

async def play_song(url):
    global voice
    if not voice:
        voice = await client.join_voice_channel(client.get_channel('407915631728656384')) 
    global player
    if not player:
        player = await voice.create_ytdl_player(url)
    else:
        player.stop()
        player = await voice.create_ytdl_player(url)
    player.start()

lists = {}

@client.event
async def on_message(message):
    if message.content.startswith('this is so sad alexa play despacito'):
        await play_song('https://www.youtube.com/watch?v=kJQP7kiw5Fk')
    elif message.content.startswith('alexa play'):
        if len(message.content.split()) >= 3:
            query = " ".join(message.content.split()[2:])
            url = search(query)[0]
            await play_song(url)
    elif message.content.startswith('!disconnect'):
        if voice:
            await voice.disconnect()
    elif (message.content.startswith("alexa what's this") or message.content.startswith('alexa whats this')):
        if message.channel != client.get_channel('336221315549888522'):
            eye = choice(eyes)
            w = choice(ws)
            await client.send_message(message.channel, f"{eye}{w}{eye}")
        else:
            client.delete_message(message)
    elif message.content.startswith('alexa create a list called'):
        name = ' '.join(message.content.split()[5:])
        if name not in lists:
            lists[name] = []
            await client.send_message(message.channel, f'Created list **{name}**')
        else:
            await client.send_message(message.channel, f'List **{name}** already exists')
    elif message.content.startswith('alexa add') and 'to' in message.content:
        split_content = message.content.split()
        to_index = split_content.index('to')
        task = ' '.join(split_content[2:to_index])
        list_name = ' '.join(split_content[to_index+1:])
        lists[list_name].append(task)
        await client.send_message(message.channel, f'Added **{task}** to **{list_name}**')
    elif message.content.startswith('alexa remove') and 'from' in message.content:
        split_content = message.content.split()
        from_index = split_content.index('from')
        task = split_content[2:from_index]
        list_name = ' '.join(split_content[from_index+1:])
        lists[list_name].remove(task)
        await client.send_message(message.channel, f'Removed **{task}** from **{list_name}**')
    elif (message.content.startswith("alexa whats on")):
        list_name = ' '.join(message.content.split()[3:])
        res = '\n'.join([f'{lists[list_name].index(item)+1}. {item}' for item in lists[list_name]])
        await client.send_message(message.channel, res)
    elif message.content.startswith('asjndoainsdpiasnodan'):
        await client.send_message(message.channel, 'holy shit bitch i stg shut the FUCK up by jove on god if you smash that keyboard one more time i will climb the fuck out of your monitor and rip you a new goddamn anus')

client.run(os.environ['ALEXA_TOKEN'])