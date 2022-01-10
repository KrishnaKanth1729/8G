import discord

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('g!'):
        if message.content == 'g!hello':
            await message.channel.send(f"Hello {message.author.mention}")
    

client.run('OTI5OTU1NDUxOTA5NTc4ODEz.Ydu2gQ.ubY63JHK1Z1FXH2n4Z2yr5RL0cQ')