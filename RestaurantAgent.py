# Importing required libraries
import assemblyai as aai
from elevenlabs import generate, stream
from openai import OpenAI
import os
from dotenv import load_dotenv

# Loading environmental variables
load_dotenv()

# Create a class for Ai Assistant
class Assistant:
    def __init__(self):
        aai.settings.api_key = os.environ["ASSEMBLYAI_API_KEY"]
        self.openai_client = OpenAI(api_key = os.environ["OPENAI_API_KEY"])
        self.elevenlabs_api_key = os.environ["ELEVENLABS_API_KEY"]

        self.transcriber = None
        
        # Prompt
        self.full_transcript = [
            {"role":"system", "content":"You are a receptionist at a restaurant. Be resourceful and efficient"}
        ]

### Real time transcription with assembly ai
    def start_transcription(self):
        print("[DEBUG] Starting transcription...")
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate = 16000,
            on_data = self.on_data,
            on_error = self.on_error,
            on_open = self.on_open,
            on_close = self.on_close,
            end_utterance_silence_threshold = 1000
        )

        self.transcriber.connect()
        print("[DEBUG] Microphone stream starting...")
        microphone_stream = aai.extras.MicrophoneStream(sample_rate = 16000)
        print("[DEBUG] Calling transcriber.stream()")
        self.transcriber.stream(microphone_stream)
        print("[DEBUG] Transcription stream active.")

    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        print(f"[DEBUG] AssemblyAI session started: {session_opened.session_id}")
        return

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return
        print(f"[DEBUG] Transcript received: {transcript.text}")

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            print("[DEBUG] Final transcript. Generating AI response.")
            self.generate_ai_response(transcript)
        else:
            print("[DEBUG] Partial transcript:", transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        # print("An error occured:", error)
        return

    def on_close(self):
        # print("Closing Session")
        return

### Pass real-time transcript to OpenAI ######
    def generate_ai_response(self, transcript):

        self.stop_transcription()
        print(f"[DEBUG] Final user input: {transcript.text}")

        self.full_transcript.append({"role":"user", "content":transcript.text})
        print(f"\nUser: {transcript.text}", end = "\r\n")

        response = self.openai_client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = self.full_transcript
        )

        ai_response = response.choices[0].message.content
        print(f"[DEBUG] AI Response: {ai_response}")

        self.gene_audio(ai_response)

        self.start_transcription()

### Generate the audio using Eleven labs
    def generate_audio(self, text):

        self.full_transcript.append({"role":"assistant", "content":text})
        print(f"\nAI Receptionist:{text}")

        audio_stream = generate(
            api_key = self.elevenlabs_api_key,
            text = text,
            voice = "Aria",
            stream = True
        )

        stream(audio_stream)

### Defining start and end of our method/function
greeting = "Thank you for calling Zafrani. My name is Amanda, how may I assist you?"
ai_assistant = Assistant()
ai_assistant.generate_audio(greeting)
ai_assistant.start_transcription()