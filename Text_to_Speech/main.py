from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from dotenv import load_dotenv
from tkinter import filedialog
import os
import sys
import subprocess
import tkinter as tk

load_dotenv(r"C:\Users\hulaspet\DEV\Python_env\.env")
VOICE_LIST = ["Olivia", "Matthew", "Amy", "Emma", "Brian", "Aria", "Ayanda", "Ivy", "Joanna", "Kendra", "Kimberly",
              "Salli", "Joey", "Justin", "Kevin"]


class TextToSpeech:
    """TTS using AWS Polly."""

    def __init__(self):
        self.session = Session(aws_access_key_id=os.getenv("tts_key"), aws_secret_access_key=os.getenv("tts_secret"))
        self.polly = self.session.client("polly", region_name="eu-central-1")
        self.output = self.response = self.voice_to_use = self.tts_text = None

    def get_dropdown(self, *args):
        """Dropdown menu to select the location of the text.
        Used with tk.OptionMenu.trace()"""
        self.voice_to_use = dropdown_voice.get()

    def get_file(self):
        """Opens a file browser to select the text file to be used for TTS."""
        text_file = filedialog.askopenfile(parent=window, mode='r', title='Choose a file', filetypes=[("txt", "*.txt")])
        if text_file:
            self.tts_text = text_file.read()
            print(self.tts_text)

    def synth_request(self):
        """Request voice synth and return the error if there is one."""
        if self.voice_to_use is None:
            self.voice_to_use = "Matthew"
        if self.tts_text is None:
            self.tts_text = text_entry.get()
        try:
            self.response = self.polly.synthesize_speech(Text=self.tts_text, OutputFormat="mp3",
                                                         VoiceId=self.voice_to_use, Engine='neural')
            self.audio_stream()

        except (BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)

    def audio_stream(self):
        """Get the audio from the response and save it to the specified location
        Exit if there is no audio or can't write the file
        If autoplay is selected it will call play_audio()"""
        if "AudioStream" in self.response:
            with closing(self.response["AudioStream"]) as stream:
                self.output = filedialog.asksaveasfilename(title="Where to save it?", defaultextension=".mp3",
                                                           filetypes=[("mp3", "*.mp3")])
                try:
                    with open(self.output, "wb") as file:
                        file.write(stream.read())
                        if autoplay.get() == 1:
                            self.play_audio()
                except IOError as error:
                    print(error)
                    sys.exit(-1)
        else:
            print("Could not stream audio")
            sys.exit(-1)

    def play_audio(self):
        """Play the audio using the default player for the system"""
        if sys.platform == "win32":
            os.startfile(self.output)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, self.output])


if __name__ == "__main__":
    window = tk.Tk()
    window.config(padx=30, pady=20)
    window.title("Text to speech tool")
    dropdown_voice = tk.StringVar(window)
    dropdown_voice.set("Matthew")
    autoplay = tk.IntVar()
    tts = TextToSpeech()

    # Labels
    dropdown_voice_label = tk.Label(text="Select a voice")
    dropdown_voice_label.grid(column=0, row=0, sticky="w")

    # Entries
    text_entry = tk.Entry(width=20)
    text_entry.insert(index=0, string="or enter the text here")
    text_entry.grid(column=1, row=1, sticky="e")

    # Buttons
    text_button = tk.Button(text="Select the text file", command=tts.get_file)
    text_button.grid(column=0, row=1, sticky="w")
    tts_start = tk.Button(text="Start TTS", width=16,
                          command=tts.synth_request)
    tts_start.grid(column=1, row=5, sticky="e", )
    dropdown_voice_menu = tk.OptionMenu(window, dropdown_voice, *VOICE_LIST)
    dropdown_voice_menu.grid(column=1, row=0, sticky="e")
    dropdown_voice_menu.config(width=14)
    dropdown_voice.trace('w', tts.get_dropdown)
    checkbox_play = tk.Checkbutton(window, text="Play after saving", variable=autoplay)
    checkbox_play.grid(column=0, row=5, sticky="w")

    window.mainloop()
