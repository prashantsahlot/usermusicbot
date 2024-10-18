import asyncio
from collections import deque
from random import randint
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from threading import Thread

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
session_string = "BQHDLbkAGypNFgSBge2_r0-6Qvt1baC1Z1lJAr9uCLSwsHYMXLwNXcg8hIcFlyqQ1n1IIJrVav0VykAmubEqUdqDdF3BM5JcZnqzZhxfAW2IKL9-rHakDVa9PBKvfGvh1SYlevChAnZbz99XnnUdjtOwdJozurglhLZ3dq6wOS55l4-X7hCtYw2kso0RHSdejynXtH1o6Z3sFEmIC_7QQfHCXHM1V95kEr3YcKBTmA4-O1GtxgbonQ0dc8sXulQx1gJRl8iPj9kI_Y09yZz2fwjsz0hClQsc1G1UhyRTwa-huTa3GH2Z-H7CtUVrHz5CNQPNXnvcoaDXoh49Hkdc1LX4872zegAAAAF_oc4VAA"

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

# Main function to keep the bot and Flask server running
if __name__ == "__main__":
    keep_alive()  # Start the Flask server
    app.run()      # Start the Pyrogram bot
