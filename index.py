from discord.ext import commands
import datetime, dotenv, datetime, sqlite3, discord, os

print("Version 1.0 by enzomtp")

bot = commands.Bot(command_prefix=commands.when_mentioned, self_bot=True)
dotenv.load_dotenv()
tracked_users = os.getenv("TRACKED_USERS").split(", ")
notification_user = os.getenv("NOTIFICATION_USER")
print(f"Tracking {len(tracked_users)} users")

# Database setup
conn = sqlite3.connect('last_seen.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS User (userid TEXT PRIMARY KEY,last_seen TEXT)''')
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

@bot.event
async def on_presence_update(before, after):
    print(f"Presence update for {after}")
    if after.id == bot.user.id:
        return
    if after.status == discord.Status.offline:
        c.execute("INSERT OR REPLACE INTO User (userid, last_seen) VALUES (?, ?)", (after.id, datetime.datetime.now()))
        conn.commit()
        if str(after.id) in tracked_users:
            user = await bot.fetch_user(notification_user)
            await user.send(f"{after.name} is now offline.")
    elif after.status != discord.Status.offline:
        if str(after.id) in tracked_users:
            user = await bot.fetch_user(notification_user)
            await user.send(f"{after.name} is now online.")
            

bot.run(os.getenv("DISCORD_TOKEN"))
conn.close()