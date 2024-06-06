from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import asyncio
import pyaudio
import os
from openai import OpenAI
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
import tkinter as tk
import threading

# Event handler for processing transcription results

#Global variables
prompt = ""

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY") # API key
)

class MyEventHandler(TranscriptResultStreamHandler):
    def __init__(self, transcript_result_stream, output_widget, file_path):
        super().__init__(transcript_result_stream)
        self.output_widget = output_widget
        self.file_path = file_path

    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        for result in results:
            for alt in result.alternatives:
                transcription = alt.transcript + "\n"
                if not result.is_partial: # If the transcription is not partial, write to file
                    self.output_widget.insert(tk.END, transcription)
                    self.output_widget.see(tk.END)
                    with open(self.file_path, "a") as f:
                        f.write(transcription)
                await asyncio.sleep(0)  # Change variable to change wait time.


# Function to start transcription
async def basic_transcribe(region: str, output_widget, stop_event):
    client = TranscribeStreamingClient(region=region)

    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=16000,
        media_encoding="pcm",
        enable_partial_results_stabilization= 'True', # Enable partial results stabilization
        partial_results_stability= 'high', # [high, low, medium] - high is recommended for most use cases
        show_speaker_label= 'True', # Enable speaker identification
    )

    async def write_chunks():
        p = pyaudio.PyAudio()
        stream_in = p.open(format=pyaudio.paInt16,
                           channels=1,
                           rate=16000,
                           input=True,
                           frames_per_buffer=1024)

        try:
            while not stop_event.is_set():
                data = stream_in.read(1024, exception_on_overflow=False)
                await stream.input_stream.send_audio_event(audio_chunk=data)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await stream.input_stream.end_stream()
            stream_in.stop_stream()
            stream_in.close()
            p.terminate()

    handler = MyEventHandler(stream.output_stream, output_widget, "transcription.txt")
    await asyncio.gather(write_chunks(), handler.handle_events())

# Function to start transcription
def start_transcription(output_widget):
    global stop_event
    stop_event = threading.Event()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(basic_transcribe("us-east-1", output_widget, stop_event))

def stop_transcription():
    global stop_event
    stop_event.set()

# ChatGPT integration ---------------------------------------

# Function to read a file
def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Function to get ChatGPT response
def get_chatgpt_response(prompt, file_content):
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You listen in real time to doctor client conversations and give relevant information about the conversation for the doctor to read. You are a doctors assistant."},
            {"role": "user", "content": prompt},
            {"role": "user", "content": file_content}
        ],
        model="gpt-3.5-turbo",
    )
    
    return chat_completion.choices[0].message.content


def on_button_click():
    if button.config('text')[-1] == 'Start Transcription':
        button.config(text='Stop Transcription')
        # Start transcription in a separate thread to not block the Tkinter event loop
        threading.Thread(target=start_transcription, args=(output_text,), daemon=True).start()
        print("Process Started")
    else:
        button.config(text='Start Transcription')
        stop_transcription()
        print("Process Stopped")
        file_path = 'transcription.txt'  # Replace with your file path
        file_content = read_file(file_path)
        # prompt = "What is the patient's medical history?"
        response = get_chatgpt_response(prompt, file_content)
        chat_text.insert(tk.END, "\nUser Prompt: " + prompt + "\nChatGPT Response: " + response + "\n----------------------------")
        chat_text.see(tk.END)

# Create the main window
root = tk.Tk()
root.title("Medical Transcription and AI Chat")

# Function to update the prompt variable
def update_prompt():
    global prompt
    prompt = prompt_textbox.get("1.0", "end-1c")  # Get text from the text box, excluding the trailing newline character

# Create labels to describe each section
tk.Label(root, text="Transcription Output:").grid(row=0, column=0, sticky=tk.W)
tk.Label(root, text="AI Chat:").grid(row=0, column=1, sticky=tk.W)
tk.Label(root, text="Enter Prompt:").grid(row=2, column=0, columnspan=2, sticky=tk.W)

# Speech Transcription section
output_text = tk.Text(root, wrap=tk.WORD, width=40, height=20) # Displays transcription output text
output_text.grid(row=1, column=0, padx=5, pady=5)

# LLM chat section
chat_text = tk.Text(root, wrap=tk.WORD, width=40, height=20) # Displays chat output text
chat_text.grid(row=1, column=1, padx=5, pady=5)

# Prompt section
prompt_textbox = tk.Text(root, wrap=tk.WORD, width=80, height=4)
prompt_textbox.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Create the button to update the prompt
update_button = tk.Button(root, text="Update", command=update_prompt, width=15, height=2)
update_button.grid(row=4, column=0, pady=20)

# Create the button
button = tk.Button(root, text="Start Transcription", command=on_button_click, width=15, height=2)
button.grid(row=4, column=0, columnspan=2, pady=20)

# Run the Tkinter event loop
root.mainloop()


# --------------------------------------- WORKING CODE ABOVE THIS LINE ---------------------------------------
