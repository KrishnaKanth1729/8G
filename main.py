import discord
from discord.ext import commands
import psycopg2
import secrets
import datetime
import schedule
from utility import reverse_dict

bot = commands.Bot(command_prefix="g!")

conn = psycopg2.connect(
    host=secrets.DB_HOST,
    database=secrets.DB_NAME,
    user=secrets.DB_USER,
    password=secrets.DB_PASSWORD
)
cursor = conn.cursor()

numbers = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
} 


@bot.command(name="poll")
async def new_poll(ctx, query: str, *args):
    """
    Create a new poll
    """
    print(*args)
    if len(args) > 9:
        return await ctx.channel.send("You can't have more than 9 options")

    for arg in args:   
        cursor.execute("INSERT INTO option(name, count) VALUES(%s,%s)", (arg, 0,))
        conn.commit()

    ids = []
    for arg in args:
        cursor.execute("SELECT option_id FROM option WHERE name=%s", (arg,))
        rows = cursor.fetchall()[0]
        ids.append(str(rows[0]))

    await ctx.message.delete()

    embed = discord.Embed(title=f"Poll by {ctx.author}", description=f"{query}", color=0x000)
    
    for i, arg in enumerate(args):
        embed.add_field(name=f"{numbers[i+1]}", value=arg, inline=False)
        
    msg = await ctx.channel.send(embed=embed)
    for i, arg in enumerate(args):
        await msg.add_reaction(f"{numbers[i+1]}")

    cursor.execute("INSERT INTO poll(title, options, author, message_id) VALUES(%s,%s,%s,%s)", (query, ",".join(ids), str(ctx.author).replace("#", "_"), str(msg.id),))
    conn.commit()

@bot.command(name="pollend")
async def end_poll(ctx):
    """
    End the latest poll of the user
    """
    cursor.execute("SELECT * FROM poll WHERE author=%s", (str(ctx.author).replace("#", "_"),))
    row = cursor.fetchall()[-1]

    poll_message = await ctx.fetch_message(int(row[-1]))
    print(int(row[-1]))
    c = {}
    for reaction in poll_message.reactions:
        if reaction.emoji in numbers.values():  # Checking if it is a number emoji
            c[reaction.emoji] = reaction.count

    c = sorted(c, key=lambda x: int(c[x])-1, reverse=True)

    options_ids = row[2].split(',')

    options = []
    for _id in options_ids:
        cursor.execute("SELECT * FROM option WHERE option_id=%s", (str(_id),))
        options.append(cursor.fetchone())
    
    r = reverse_dict(numbers)
    res = []

    for item in c:
        res.append(r[item]-1)
    
    embed = discord.Embed(title=f"Poll results", description=f"{row[1]}", color=0x000)
    
    for i, item in enumerate(res):
        embed.add_field(name=f"**{i+1}**. {options[item][1]}", value=f"|", inline=True)
    
    await ctx.channel.send(embed=embed)

@bot.command(name="create_tag")
async def create_tag(ctx, title: str, content: str):
    cursor.execute("SELECT * FROM tag WHERE name=%s", (title,))
    rows = cursor.fetchall()

    if len(rows):
        return await ctx.channel.send("Tag with that name already exists")
    
    cursor.execute('INSERT INTO tag(name, content, author) VALUES(%s,%s,%s)', (title, content, str(ctx.author).replace("#", "_")))  
    conn.commit()
    await ctx.channel.send(f"Tag successfully created")

@bot.command(name="tag")
async def tag(ctx, title: str):
    cursor.execute("SELECT * FROM tag WHERE name=%s", (title,))
    rows = cursor.fetchall()
            
    try:
        result = rows[0]
        await ctx.channel.send(f"{result[2]} \n **Author**: {result[3].replace('_', '#')}")
    except:
        await ctx.channel.send(f"Tag with name {title} is not found")

def send_reminder(content):
    general = bot.get_channel(secrets.GENERAL_CHANNEL_ID)
    general.send(f"@everyone {content}")

@bot.command(name="schedule")
async def create_schedule_reminder(ctx, title: str, content: str, time: str):
    schedule.every().day.at(time).do(send_reminder, f"{title}: {content}")
    await ctx.channel.send("Done")
    
bot.run(secrets.BOT_TOKEN)