import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

# Loads environment variables from the .env file
load_dotenv()

# Set up necessary Discord intents
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True

# Initialize the bot with a command prefix and the specified intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Load the announcement channel ID from the environment
ANNOUNCE_CHANNEL_ID = os.getenv("ANNOUNCE_CHANNEL_ID")    

# Emojis used for different types of voice channel events
EMOJIS = {
    "join": ["🎧", "👋", "🙌", "✨", "🎶"],
    "switch": ["🔄", "🛫", "🌀", "➡️"],
    "leave": ["👋", "💨", "❌", "🚪"]
}

# Helper function to generate a random RGB color for embeds
def random_color():
    return discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Called when the bot successfully connects and is ready
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and ready!")

# Event handler for any voice state changes (join, leave, or switch channels)
@bot.event
async def on_voice_state_update(member, before, after):
    # Only proceed if the voice channel actually changed
    if before.channel != after.channel:
        announce_channel = bot.get_channel(ANNOUNCE_CHANNEL_ID)
        if not announce_channel:
            return

         # Member joined a voice channel
        if before.channel is None and after.channel is not None:
            emoji = random.choice(EMOJIS["join"])
            title = f"{emoji} {member.display_name} joined voice!"
            description = f"**{member.mention}** joined **{after.channel.name}**"
        
        # Member switched between two voice channels
        elif before.channel is not None and after.channel is not None:
            emoji = random.choice(EMOJIS["switch"])
            title = f"{emoji} {member.display_name} switched channels!"
            description = f"**{member.mention}** moved from **{before.channel.name}** to **{after.channel.name}**"

        # Member left a voice channel
        elif before.channel is not None and after.channel is None:
            emoji = random.choice(EMOJIS["leave"])
            title = f"{emoji} {member.display_name} left voice"
            description = f"**{member.mention}** left **{before.channel.name}**"

        else:
            return

        # Create an embed and send it to the announcement channel
        embed = discord.Embed(
            title=title,
            description=description,
            color=random_color()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await announce_channel.send(embed=embed)
        
# Load the bot token from environment and start the bot 
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(DISCORD_TOKEN)