import discord
import sqlite3
import secrets

conn = sqlite3.connect("tags.db")
cursor = conn.cursor()
client = discord.Client()

cursor.execute("CREATE TABLE IF NOT EXISTS tags(id integer PRIMARY KEY AUTOINCREMENT, name text, content text, author text)")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith('g!'):
        if message.content == 'g!hello':
            await message.channel.send(f"Hello {message.author.mention}", reference=message)
    
        elif message.content.startswith('g!create'):
            items = message.content.split()
            name = items[1]
            content = " ".join(items[2:])
            author = str(message.author).replace('#', '_')
            print(name, content, author)
            cursor.execute(f"SELECT * FROM tags WHERE name=?", (name,))
            rows = cursor.fetchall()
            print(rows)
            if len(rows):
                return await message.channel.send("Tag with that name already exists", reference=message)
            cursor.execute('INSERT INTO tags(name, content, author) VALUES(?, ?, ?)', (name, content, author))
           
            conn.commit()
            await message.channel.send(f"Tag successfully created", reference=message)

        elif message.content.startswith('g!tag'):
            items = message.content.split()
            name = items[1]
            cursor.execute(f"SELECT * FROM tags WHERE name=?", (name,))
            rows = cursor.fetchall()
            print(rows)
client.run(secrets.TOKEN)