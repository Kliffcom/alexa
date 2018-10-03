import discord
import os
from search import search
from random import choice
import asyncio
import youtube_dl
import discord.ext.commands as ext

bot = ext.Bot(command_prefix=['!', 'alexa '])

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
voice = None
player = None
eyes = [':eye:', ':eye_in_speech_bubble:', ':regional_indicator_o:', ':white_circle:']
ws = [':snake:', ':cactus:', ':part_alternation_mark:', ':aries:', ':regional_indicator_w:']
lists = {}

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.duration = data.get('duration')
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

async def play_song(url):
    global voice
    if not voice:
        voice = await bot.get_channel(407915631728656384).connect()
    global player
    if not player:
        player = await YTDLSource.from_url(url=url, stream=True)
    else:
        voice.stop()
        player = await YTDLSource.from_url(url=url, stream=True)
    voice.play(player)

@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(f"discord.py {discord.__version__}")
    print('------')

@bot.event
async def on_message(message):
    #rewrite
    if message.content.startswith('this is so sad alexa play despacito'):
        await play_song('https://www.youtube.com/watch?v=kJQP7kiw5Fk')
    elif message.content.startswith('asjndoainsdpiasnodan'):
        await message.channel.send('holy shit bitch i stg shut the FUCK up by jove on god if you smash that keyboard one more time i will climb the fuck out of your monitor and rip you a new goddamn anus')
    else:
        await bot.process_commands(message)

@bot.command(name='play')
async def alexa_play(ctx):
    """Plays a song from a youtube link
    Usage: alexa play <youtube-link>
    """
    if len(ctx.message.content.split()) >= 3:
        query = " ".join(ctx.message.content.split()[2:])
        url = search(query)[0]
        await play_song(url)

@bot.command(name='disconnect')
async def disconnect(ctx):
    """Disconnects the Bot from the current Voice Channel"""
    global voice
    global player
    if voice:
        await voice.disconnect()
    voice = None
    player = None

@bot.group(name='whats', aliases=["what's"], hidden=True)
async def alexa_what(ctx):
    if ctx.invoked_subcommand is None:
        return

@alexa_what.command(name='this')
async def alexa_whats_is(ctx):
    """ʘwʘ"""
    if not ctx.message.channel.id == 336221315549888522:
        eye = choice(eyes)
        w = choice(ws)
        await ctx.message.channel.send(f"{eye}{w}{eye}")
    else:
        await ctx.message.delete()

@bot.command(name='create')
async def alexa_create(ctx):
    """Creates a list with a custom name
    Usage: alexa create a list called <name>
    """
    if not 'a list called' in ctx.message.content:
        return
    name = ' '.join(ctx.message.content.split()[5:])
    if name not in lists:
        lists[name] = []
        await ctx.message.channel.send(f'Created list **{name}**')
    else:
        await ctx.message.channel.send(f'List **{name}** already exists')

@bot.command(name='add')
async def alexa_add(ctx):
    """Adds a Entry to a list
    Usage: alexa add <entry> to <list>
    """
    if not 'to' in ctx.message.content:
        return
    split_content = ctx.message.content.split()
    to_index = split_content.index('to')
    task = ' '.join(split_content[2:to_index])
    list_name = ' '.join(split_content[to_index+1:])
    lists[list_name].append(task)
    print(lists[list_name])
    await ctx.message.channel.send(f'Added **{task}** to **{list_name}**')

@bot.command(name='remove')
async def alexa_remove(ctx):
    """Removes a Entry to a list
    Usage: alexa remove <entry> from <list>
    """
    if not 'from' in ctx.message.content:
        return
    split_content = ctx.message.content.split()
    from_index = split_content.index('from')
    task = split_content[2:from_index][0]
    list_name = ' '.join(split_content[from_index+1:])
    lists[list_name].remove(task)
    await ctx.message.channel.send(f'Removed **{task}** from **{list_name}**')

@alexa_what.command(name='on')
async def alexa_whats_on(ctx):
    """Displays all entries on a list
    Usage: alexa whats on <list>
    """
    list_name = ' '.join(ctx.message.content.split()[3:])
    res = '\n'.join([f'{lists[list_name].index(item)+1}. {item}' for item in lists[list_name]])
    await ctx.message.channel.send(res)

bot.run(os.environ['ALEXA_TOKEN'])
