# TODO:
#   2. Make a GUI to either open a file to process or type in some text, select different voices
#   3. Add option to save the file or just open it right away

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from tempfile import gettempdir
from dotenv import load_dotenv
import os
import sys
import subprocess

load_dotenv(r"C:\Users\hulaspet\DEV\Python_env\.env")

# Temp place here, will have a GUI for it
text_to_read = "This is just some random text here"
voice_to_use = "Matthew"


class TextToSpeech:
    def __init__(self):
        self.session = Session(aws_access_key_id=os.getenv("tts_key"), aws_secret_access_key=os.getenv("tts_secret"))
        self.polly = self.session.client("polly", region_name="eu-central-1")
        self.output = None
        self.response = None

    def synth_request(self):
        """Request voice synth and return the error if there is one."""
        try:
            self.response = self.polly.synthesize_speech(Text=text_to_read, OutputFormat="mp3",
                                                         VoiceId=voice_to_use, Engine='neural')
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
    tts = TextToSpeech()
    tts.synth_request()
    tts.audio_stream()
    tts.play_audio()
