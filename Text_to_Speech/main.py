#TODO:
#   1. Fix the class, this is for testing only
#   2. Make a GUI to either open a file to process or type in some text
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

text_to_read = "Some text here"


class TextToSpeech:
    def __init__(self):
        self.session = Session(aws_access_key_id=os.getenv("tts_key"), aws_secret_access_key=os.getenv("tts_secret"))
        self.polly = self.session.client("polly", region_name="eu-central-1")

    def other(self):
        try:
            # Request speech synthesis
            response = self.polly.synthesize_speech(Text=text_to_read, OutputFormat="mp3",
                                               VoiceId="Matthew", Engine='neural')
            print(response)
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print(error)
            sys.exit(-1)
        
        # Access the audio stream from the response
        if "AudioStream" in response:
            # Note: Closing the stream is important because the service throttles on the
            # number of parallel connections. Here we are using contextlib.closing to
            # ensure the close method of the stream object will be called automatically
            # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(gettempdir(), "speech.mp3")
        
                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)
        
        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)
        
        # Play the audio using the platform's default player
        if sys.platform == "win32":
            os.startfile(output)
        else:
            # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, output])
    
if __name__ == "__main__":
    tts = TextToSpeech()
    tts.other()
