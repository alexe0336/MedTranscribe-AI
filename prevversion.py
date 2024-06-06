import asyncio
import pyaudio
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent
import tkinter as tk
import threading

# Event handler for processing transcription results
class MyEventHandler(TranscriptResultStreamHandler):
    def __init__(self, transcript_result_stream, output_widget):
        super().__init__(transcript_result_stream)
        self.output_widget = output_widget

    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        for result in results:
            for alt in result.alternatives:
                self.output_widget.insert(tk.END, alt.transcript + "\n")
                self.output_widget.see(tk.END)
                await asyncio.sleep(0) # Change vairable to change wait time.

# Function to start transcription
async def basic_transcribe(region: str, output_widget, stop_event):
    client = TranscribeStreamingClient(region=region)

    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=16000,
        media_encoding="pcm",
        # show_speaker_label= True, # Enable speaker identification
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

    handler = MyEventHandler(stream.output_stream, output_widget)
    await asyncio.gather(write_chunks(), handler.handle_events())

def start_transcription(output_widget):
    global stop_event
    stop_event = threading.Event()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(basic_transcribe("us-east-1", output_widget, stop_event))

def stop_transcription():
    global stop_event
    stop_event.set()

# Function to handle button click
def on_button_click():
    if button.config('text')[-1] == 'Start':
        button.config(text='Stop')
        # Start transcription in a separate thread to not block the Tkinter event loop
        threading.Thread(target=start_transcription, args=(output_text,), daemon=True).start()
        print("Process Started")
    else:
        button.config(text='Start')
        stop_transcription()
        print("Process Stopped")

# Create the main window
root = tk.Tk()
root.title("Real Time Voice Transcription")

# Create the ScrolledText widget to display transcriptions
output_text = tk.Text(root, wrap=tk.WORD, width=80, height=20)
output_text.pack(pady=10)

# Create the button
button = tk.Button(root, text="Start", command=on_button_click, width=15, height=2)
button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
# --------------------------------------- WORKING CODE ABOVE THIS LINE ---------------------------------------