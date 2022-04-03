# TODO:
#   2. Make a GUI to either open a file to process or type in some text, select different voices
#   3. Add option to save the file or just open it right away

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from tempfile import gettempdir
from dotenv import load_dotenv
from tkinter import filedialog
import os
import sys
import subprocess
import tkinter as tk


load_dotenv(r"C:\Users\hulaspet\DEV\Python_env\.env")

# Temp place here, will have a GUI for it
text_to_read = "This is just some random text here"
#voice_to_use = "Matthew"
voice_list = ["Olivia", "Matthew", "Amy", "Emma", "Brian", "Aria", "Ayanda", "Ivy", "Joanna", "Kendra", "Kimberly",
              "Salli", "Joey", "Justin", "Kevin"]




class TextToSpeech:
    def __init__(self):
        self.session = Session(aws_access_key_id=os.getenv("tts_key"), aws_secret_access_key=os.getenv("tts_secret"))
        self.polly = self.session.client("polly", region_name="eu-central-1")
        self.output = None
        self.response = None
        self.voice_to_use = None

    def get_dropdown(self, *args):
        """Dropdown menu to select the location of the text.
        Used with tk.OptionMenu.trace()"""
        self.voice_to_use = dropdown.get()


    def synth_request(self):
        """Request voice synth and return the error if there is one."""
        if self.voice_to_use is None:
            self.voice_to_use = "Matthew"
        try:
            self.response = self.polly.synthesize_speech(Text=text_entry.get(), OutputFormat="mp3",
                                                         VoiceId=self.voice_to_use, Engine='neural')
            self.audio_stream()

        except (BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)

    def audio_stream(self):
        """Get the audio from the response
        Exit if there is no audio or can't write the file"""
        if "AudioStream" in self.response:
            with closing(self.response["AudioStream"]) as stream:
                self.output = os.path.join(gettempdir(), "speech.mp3")
                try:
                    with open(self.output, "wb") as file:
                        file.write(stream.read())
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
    #tts.synth_request()
    #tts.audio_stream()
    #tts.play_audio()

    window = tk.Tk()
    window.config(padx=30, pady=20)
    window.title("Text to speech tool")
    dropdown = tk.StringVar(window)
    dropdown.set("Matthew")
    tts = TextToSpeech()

    # Labels
    text_label = tk.Label(text="Text:")
    text_label.grid(column=0, row=1, sticky="w")
    dropdown_label = tk.Label(text="Select a voice")
    dropdown_label.grid(column=0, row=0)

    # Entries
    text_entry = tk.Entry(width=20)
    text_entry.insert(index=0, string="Enter the text")
    text_entry.grid(column=1, row=1, sticky="w")

    # Buttons
    tts_start = tk.Button(text="Start TTS", width=16,
                          command=tts.synth_request)
    tts_start.grid(column=1, row=4, sticky="w",)
    #color_button = tk.Button(text="Browse color", width=20, command=get_color)
    #color_button.grid(column=1, row=2, sticky="w")
    dropdown_menu = tk.OptionMenu(window, dropdown, *voice_list)
    dropdown_menu.grid(column=1, row=0, sticky="w")
    dropdown_menu.config(width=14)
    dropdown.trace('w', tts.get_dropdown)

    window.mainloop()


