import asyncio
from collections import deque
from datetime import datetime
from random import randint
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask, jsonify
from threading import Thread
import os

# Flask app to handle the port issue
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "Bot is running!"

# Health check endpoint
@app_flask.route("/ping")
def ping():
    return jsonify({"status": "alive"})

# Function to run the Flask app on port 8080
def run_flask():
    app_flask.run(host="0.0.0.0", port=8080)

# Function to keep the Flask app running in a separate thread
def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# Your session string (ensure you store this securely)
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

    # Check if the command was issued as a reply
    if message.reply_to_message:
        user_ = message.reply_to_message.from_user
        if user_:
            user_id = user_.id  # Get the user ID from the replied message
        else:
            await message.edit("`Could not retrieve the user ID from the replied message.`")
            return
    else:
        # Split the message text and check if an argument was provided
        args = message.text.split()
        
        if len(args) < 2:
            await message.edit("`Please provide a username or user ID to clone or reply to a user's message.`")
            return
        
        user_id = args[1]

    # Start cloning process
    op = await message.edit("`Cloning...`")  # Initial message
    
    try:
        user_ = await client.get_users(user_id)
        await op.edit("`User found. Fetching user information...`")  # Edit message to show user found
    except Exception:
        await op.edit("`User not found.`")
        return

    user_info = await client.get_chat(user_.id)
    original_name = user_.first_name
    original_bio = user_info.bio if user_info.bio else "join - @frozensupport1"
    
    pic = user_.photo.big_file_id if user_.photo else None
    if pic:
        await op.edit("`Downloading profile picture...`")  # Edit to indicate picture download
        photo = await client.download_media(pic)
        await client.set_profile_photo(photo=photo)
        await op.edit("`Profile picture set.`")  # Edit to indicate picture set

    await op.edit("`Updating profile...`")  # Edit to indicate profile update
    await client.update_profile(
        first_name=original_name,
        bio=original_bio,
    )
    
    await op.edit(f"**From now on, I'm** __{original_name}__")  # Final message


@app.on_message(filters.command("revert", ".") & filters.me)
async def revert(client: Client, message: Message):
    await message.edit("`Reverting...`")
    
    # Check if original name and bio are set
    if not original_name or not original_bio:
        await message.edit("`Original name or bio not set.`")
        return

    try:
        # Update profile back to original name and bio
        await client.update_profile(
            first_name=original_name,
            bio=original_bio,
        )

        # Delete the first photo to revert to your original identity
        photos = [p async for p in client.get_chat_photos("me")]
        if photos:
            await client.delete_profile_photos(photos[0].file_id)

        await message.edit("`I am back to my original identity!`")
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
    await e.edit("💖 You're my star 💖")

# Delete command
@app.on_message(filters.command("del", ".") & filters.me)
async def del_msg(client: Client, message: Message):
    msg_src = message.reply_to_message
    if msg_src:
        if msg_src.from_user.id:
            try:
                await client.delete_messages(message.chat.id, msg_src.id)
                await message.delete()
            except BaseException:
                pass
    else:
        await message.delete()

# Purge command
@app.on_message(filters.command("purge", ".") & filters.me)
async def purge(client: Client, message: Message):
    ex = await message.edit_text("`Starting To Purge Messages!`")
    msg = message.reply_to_message
    if msg:
        itermsg = list(range(msg.id, message.id))
    else:
        await ex.edit("`Reply To Message To Purge!`")
        return
    count = 0

    for i in itermsg:
        try:
            count += 1
            await client.delete_messages(
                chat_id=message.chat.id, message_ids=i, revoke=True
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await ex.edit(f"**ERROR:** `{e}`")
            return

    done = await ex.edit(
        f"**Fast Purge Completed!**\n**Successfully Delete** `{str(count)}` **Message.**"
    )
    await asyncio.sleep(2)
    await done.delete()

# Purge me command
@app.on_message(filters.command("purgeme", ".") & filters.me)
async def purgeme(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.delete()
    n = message.text.split(None, 1)[1].strip()
    if not n.isnumeric():
        return await message.edit_text("Please enter a number")
    n = int(n)
    if n < 1:
        return await message.edit_text("Enter the number of messages you want to delete!")
    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in client.search_messages(
            chat_id,
            from_user="me",
            limit=n,
        )
    ]
    if not message_ids:
        return await message.edit_text("Could not find message.")
    to_delete = [message_ids[i: i + 99] for i in range(0, len(message_ids), 99)]
    for hundred_messages_or_less in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
    await message.delete()

# Start the bot and Flask app
if __name__ == "__main__":
    keep_alive()
    app.run()  # Start the Pyrogram Client



