# 8G Discord-Bot

A general-purpose discord bot for the 8G Discord-Server


To setup:

The app uses `PostgreSQL`
create a database and then get the details and fill it in `secrets.py`

1. Create a new file called `secrets.py` and make it look like this
```py
BOT_TOKEN = "********************"
MUTED_ROLE_ID = 1234567890
GENERAL_CHANNEL_ID = 1234567890
DB_HOST = "localhost"
DB_NAME = '8gbot'
DB_USER = 'postgres'
DB_PASSWORD = '***********'
```

Get your token from https://discord.com/developers/applications
Create a new application, add a bot to that, get the bot token and paste it in `secrets.py` after TOKEN= in line number 1 and change the db file name if you want so

2. Install all requirements 
```py
pip install -r requirements.txt
```

3. Run the main file
```py
python main.py
```

# Core developers
KrishnaKanth1729 <br>
PranavSudhakarSG <br>
ShikharKonnur