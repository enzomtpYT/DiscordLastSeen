from discord.ext import commands
import datetime
import dotenv
import sqlite3
import discord
import os

print("Version 1.1 by enzomtp")

bot = commands.Bot(command_prefix=commands.when_mentioned, self_bot=True)
dotenv.load_dotenv()
tracked_users = os.getenv("TRACKED_USERS").split(", ")
notification_user = int(os.getenv("NOTIFICATION_USER"))
print(f"Tracking {len(tracked_users)} users")

# Database setup
conn = sqlite3.connect('last_seen.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS User (userid TEXT PRIMARY KEY, last_seen TEXT)''')
conn.commit()

@bot.command(aliases=["ls"])
async def lastseen(ctx, user: discord.User = None):
    print(f"Command executed by {ctx.author.name}")
    if not ctx.author.id == bot.user.id:
        return
    if user is None:
        c.execute("SELECT userid, last_seen FROM User")
        users = c.fetchall()
        if users:
            message = "Last seen times:\n"
            for userid, last_seen in users:
                user = await bot.fetch_user(userid)
                message += f"{user.name}: {last_seen}\n"
            await ctx.send(message)
        else:
            await ctx.send("No records found.")
    else:
        c.execute("SELECT last_seen FROM User WHERE userid = ?", (user.id,))
        result = c.fetchone()
        if result:
            last_seen_time = result[0]
            await ctx.send(f"{user.name} was last seen at {last_seen_time}")
        else:
            await ctx.send(f"No record of {user.name}")

@bot.event
async def on_ready():
    print(f'Connected to discord with: {bot.user.name}')

# Dictionary to store the last known status of each user
last_status = {}

@bot.event
async def on_presence_update(before, after):
    if after.id == bot.user.id:
        return
    if before.status == after.status:
        return  # Status hasn't changed, so we ignore this event
    if after.id in last_status and last_status[after.id] == after.status:
        return  # Status hasn't changed since the last update, so we ignore this event
    last_status[after.id] = after.status  # Update the last known status

    if after.status == discord.Status.offline:
        c.execute("INSERT OR REPLACE INTO User (userid, last_seen) VALUES (?, ?)", (after.id, datetime.datetime.now()))
        conn.commit()
        if str(after.id) in tracked_users:
            try:
                user_profile = await bot.fetch_user_profile(notification_user, with_mutual_guilds=True)
                await user_profile.send(f"<@{after.id}> is now offline.")
            except discord.errors.NotFound:
                print(f"User with ID {notification_user} not found.")
            except discord.errors.HTTPException as e:
                print(f"HTTP exception occurred: {e}")
    elif after.status != discord.Status.offline:
        if str(after.id) in tracked_users:
            try:
                user_profile = await bot.fetch_user_profile(notification_user, with_mutual_guilds=True)
                await user_profile.send(f"<@{after.id}> is now online.")
            except discord.errors.NotFound:
                print(f"User with ID {notification_user} not found.")
            except discord.errors.HTTPException as e:
                print(f"HTTP exception occurred: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
conn.close()