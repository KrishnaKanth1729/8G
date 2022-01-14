import secrets
import psycopg2

conn = psycopg2.connect(
    host=secrets.DB_HOST,
    database=secrets.DB_NAME,
    user=secrets.DB_USER,
    password=secrets.DB_PASSWORD
)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS tag(tag_id SERIAL PRIMARY KEY, name text, content text, author text)")
cursor.execute("CREATE TABLE IF NOT EXISTS option(option_id SERIAL PRIMARY KEY, name text, count integer)")
cursor.execute("CREATE TABLE IF NOT EXISTS poll(poll_id SERIAL PRIMARY KEY, title text, options text, author text, message_id text)")
cursor.execute("CREATE TABLE IF NOT EXISTS reminder(reminder_id SERIAL PRIMARY KEY, title text, about text, time text")

conn.commit()
