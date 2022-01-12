import discord
import sqlite3
import secrets

conn = sqlite3.connect(secrets.DB_FILENAME)
cursor = conn.cursor()
client = discord.Client()

cursor.execute("CREATE TABLE IF NOT EXISTS tags(id integer PRIMARY KEY AUTOINCREMENT, name text, content text, author text)")
cursor.execute("CREATE TABLE IF NOT EXISTS")
cursor.execute("CREATE TABLE IF NOT EXISTS poll(id integer PRIMARY KEY AUTOINCREMENT, title text, options")

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
            if message.mentions:
                return await message.channel.send("There's a mention in the tag")
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
            try:
                result = rows[0]
                await message.channel.send(f"{result[2]} \n **Author**: {result[3].replace('_', '#')}")
            except:
                await message.channel.send(f"Tag with name {name} is not found")
client.run(secrets.TOKEN)