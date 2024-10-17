from pytgcalls import PyTgCalls
from pytgcalls import idle
from pytgcalls.types import MediaStream
from pyrogram import Client, filters

# Your session string
session_string = "BQHDLbkAGk1NVxfUnxNAUfpaq6ygc242zXXDGSs1FDRJHRHBwmFK993Q7Yq-CorDxXgHWSenkFZ7wZG-noz7D44cjcCtzi7dwkwzkPiG4tjLHWSaeqRzgrpCn995k6i3s9bkQ1PFImNZ8sYRuW-dcrbFR53brHNfJCek-dT9-DGfKUvm1deBxEsg4NfQM3-p7ifXHt1jEh0cl1tL0RwY89vDu-3Ibr9J9g3hHNR1CC-75im2qZWiPIPFHIhVWqshUvIDYeGDEf9pgW-uTrrDPl87EZdX33Jehmf54YjlGkN2dgP3-0XfIhB1z5Hozl7jHW_Bl5husowsQT5-T-TWjkW_nEi9ngAAAAF_oc4VAA"

# Change the path to where you want to save the session
app = Client("my_bot", api_id=29568441, api_hash="b32ec0fb66d22da6f77d355fbace4f2a", session_string=session_string, workdir=r"C:\Users\PC\Documents\session.txt")

# Initialize PyTgCalls
tg_calls_app = PyTgCalls(app)

# Start the client
app.start()
tg_calls_app.start()

# Define the /play command handler
@app.on_message(filters.command("play"))
def play_command_handler(client, message):
    # Use the specified streaming URL
    video_url = 'http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4'
    
    try:
        tg_calls_app.play(
            message.chat.id,
            MediaStream(video_url),
        )
        message.reply_text("🎥 Now playing the video!")
    except Exception as e:
        message.reply_text(f"An error occurred: {e}")

# Keep the script running
idle()
