import asyncio
from collections import deque
from random import randint
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from threading import Thread
import os

# Flask app to handle the port issue
app_flask = Flask("")

@app_flask.route("/")
def home():
    return "Bot is running!"

# Function to run the Flask app on port 8080
def run():
    app_flask.run(host="0.0.0.0", port=8080)

# Function to keep the Flask app running in a separate thread
def keep_alive():
    t = Thread(target=run)
    t.start()

# Your session string
session_string = "BQHDLbkAToe1oK66Cdo-dJg6dECM0TC0OrtiLdEgXj7lBbRxfBWMfkATh7A-Gr1I8by8Lv8KOTYRtaDpL1FMQZPLQS2x0pQ3pRinrLdm4tSfCK3HsRstE_THT1539M9-moRj5UVwY53QQa6SWBSnTtXgWuDEF5tbdVbabVl0Li6SyxVbIj7pQ3QyG4R9wCECBnLee9XEtsyvDSs2_4BneNUMv5e6Alrjrz4iCV1wbkpScP8I0pYvX8xU_Wt2ahVzYEr5ARwyRY8Bl_1csK5fdyOYv9WcBh8lPt_aaC6V_9Xrimc3t1mGcX3WVNF100qBCcaRrxh93OhCKqxf_mhX-GU6IYDibgAAAAGhyyf_AA"

# Initialize the Pyrogram Client
app = Client("my_bot", api_id=29568441, api_hash="b32ec0fb66d22da6f77d355fbace4f2a", session_string=session_string)

# Emoji definitions
emojis = {
    "moon": list("🌗🌘🌑🌒🌓🌔🌕🌖"),
    "clock": list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"),
    "thunder": list("☀️🌤⛅️🌥☁️🌩🌧⛈⚡️🌩🌧🌦🌥⛅️🌤☀️"),
    "earth": list("🌏🌍🌎🌎🌍🌏🌍🌎"),
    "heart": list("❤️🧡💛💚💙💜🖤"),
}

emoji_commands = [x for x in emojis]

# Emoji cycling command
@app.on_message(filters.command(emoji_commands, ".") & filters.me)
async def emoji_cycle(bot: Client, message: Message):
    deq = deque(emojis[message.command[0]])
    try:
        for _ in range(randint(16, 32)):
            await asyncio.sleep(0.3)
            await message.edit("".join(deq), parse_mode=None)
            deq.rotate(1)
    except Exception:
        await message.delete()

# Special emoji definitions
special_emojis_dict = {
    "target": {"emoji": "🎯", "help": "The special target emoji"},
    "dice": {"emoji": "🎲", "help": "The special dice emoji"},
    "bb": {"emoji": "🏀", "help": "The special basketball emoji"},
    "soccer": {"emoji": "⚽️", "help": "The special football emoji"},
}

special_emoji_commands = [x for x in special_emojis_dict]

# Special emojis command
@app.on_message(filters.command(special_emoji_commands, ".") & filters.me)
async def special_emojis(bot: Client, message: Message):
    emoji = special_emojis_dict[message.command[0]]
    await message.delete()
    await bot.send_dice(message.chat.id, emoji["emoji"])

# Help section for commands
special_emoji_help = [
    [".moon", "Cycles all the phases of the moon emojis."],
    [".clock", "Cycles all the phases of the clock emojis."],
    [".thunder", "Cycles thunder."],
    [".heart", "Cycles heart emojis."],
    [".earth or .globe", "Make the world go round."],
]

# Add help for special emojis
for x in special_emojis_dict:
    special_emoji_help.append([f".{x}", special_emojis_dict[x]["help"]])

@app.on_message(filters.command("help") & filters.me)
async def help_command(bot: Client, message: Message):
    help_text = "Here are the available commands:\n"
    for command, description in special_emoji_help:
        help_text += f"{command}: {description}\n"
    
    await message.reply(help_text)

# Clone and revert features
OWNER = os.environ.get("OWNER", None)
BIO = os.environ.get("BIO", "404 : Bio Lost")

# Global variables to store original name and bio
original_name = None
original_bio = None

@app.on_message(filters.command("clone", ".") & filters.me)
async def clone(client: Client, message: Message):
    global original_name, original_bio  # Access global variables

    # Save the original name and bio before cloning
    user_info = await client.get_me()
    original_name = user_info.first_name  # Save original name
    original_bio = user_info.bio if user_info.bio else "No bio available."  # Save original bio

    # Check if the command was issued as a reply
    if message.reply_to_message:
        user_ = message.reply_to_message.from_user
        if user_:
            text = user_.id  # Get the user ID from the replied message
        else:
            await message.edit("`Could not retrieve the user ID from the replied message.`")
            return
    else:
        # Split the message text and check if an argument was provided
        args = message.text.split()
        
        if len(args) < 2:
            await message.edit("`Please provide a username or user ID to clone or reply to a user's message.`")
            return
        
        text = args[1]
    
    op = await message.edit_text("`Cloning`")
    
    try:
        user_ = await client.get_users(text)
    except Exception:
        await op.edit("`User not found.`")
        return

    get_bio = await client.get_chat(user_.id)
    f_name = user_.first_name
    c_bio = get_bio.bio if get_bio.bio else "No bio available."
    
    pic = user_.photo.big_file_id if user_.photo else None
    if pic:
        poto = await client.download_media(pic)
        await client.set_profile_photo(photo=poto)

    await client.update_profile(
        first_name=f_name,
        bio=c_bio,
    )
    await message.edit(f"**From now on, I'm** __{f_name}__")


@app.on_message(filters.command("revert", ".") & filters.me)
async def revert(client: Client, message: Message):
    await message.edit("`Reverting`")
    
    # Check if original name and bio are set
    if not original_name or not original_bio:
        await message.edit("`Owner or Bio not set.`")
        return

    try:
        # Get your name back
        await client.update_profile(
            first_name=original_name,
            bio=original_bio,
        )

        # Delete first photo to revert to your original identity
        photos = [p async for p in client.get_chat_photos("me")]
        if photos:
            await client.delete_profile_photos(photos[0].file_id)

        await message.edit("`I am back!`")
    except Exception as e:
        await message.edit(f"`Error reverting: {str(e)}`")



@app.on_message(filters.command(["sayang", "lover"], ".") & filters.me)
async def zeyenk(client: Client, message: Message):
    e = await message.reply("I LOVEE YOUUU 💕")
    await e.edit("💝💘💓💗")
    await e.edit("💞💕💗💘")
    await e.edit("💝💘💓💗")
    await e.edit("💞💕💗💘")
    await e.edit("💘💞💗💕")
    await e.edit("💘💞💕💗")
    await e.edit("LOVE YOU 💝💖💘")
    await e.edit("💝💘💓💗")
    await e.edit("💞💕💗💘")
    await e.edit("💘💞💕💗")
    await e.edit("LOVE")
    await e.edit("YOU")
    await e.edit("FOREVER 💕")
    await e.edit("💘💘💘💘")
    await e.edit("LOVE")
    await e.edit("I")
    await e.edit("LOVE")
    await e.edit("BABY")
    await e.edit("I LOVE YOUUUU")
    await e.edit("MY BABY")
    await e.edit("💕💞💘💝")
    await e.edit("💘💕💞💝")
    await e.edit("LOVE YOU 💞")
    # New messages to be added
    await e.edit("💖 You're my everything! 💖")
    await e.edit("You make my heart smile! 😊")
    await e.edit("You're my sunshine on a cloudy day! ☀️")
    await e.edit("Forever and always, my love! 🌹")
    await e.edit("You mean the world to me! 🌍💖")

# Main function to keep the bot and Flask server running
if __name__ == "__main__":
    keep_alive()  # Start the Flask server
    app.run()      # Start the Pyrogram bot
