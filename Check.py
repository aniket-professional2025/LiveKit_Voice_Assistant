# from elevenlabs import voices
# from dotenv import load_dotenv
# import os

# load_dotenv()
# os.environ["ELEVENLABS_API_KEY"]

# for v in voices():
#     print(f"{v.name} — ID: {v.voice_id}")

import sounddevice as sd
duration = 7  # seconds
print("Speak into your microphone...")
audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1)
sd.wait()
print("Audio captured.")