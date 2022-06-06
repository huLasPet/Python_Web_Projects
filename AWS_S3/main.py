import logging
from boto3 import Session
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
from tkinter import filedialog
import tkinter as tk



load_dotenv(r"/Users/nbyy/Library/CloudStorage/OneDrive-Personal/Python Round 2/IntelliJ/env")
REGION_LIST = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-central-1"]

class S3:
    def __init__(self):
        self.file_to_upload = None
        self.session = Session(aws_access_key_id=os.getenv("aws_s3_key"), aws_secret_access_key=os.getenv("aws_s3_secret"))

    def create_bucket(self):
        try:
            s3_client = self.session.client('s3', region_name=select_region.get())
            location = {'LocationConstraint': select_region.get()}
            s3_client.create_bucket(Bucket=bucket_entry.get(),
                                        CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            bucket_status = tk.Label(text=e.response["Error"]["Code"])
            bucket_status.grid(column=6, row=0, sticky="w")
            return False
        bucket_status = tk.Label(text="Creation successful")
        bucket_status.grid(column=6, row=0, sticky="w")
        return True

    def list_buckets(self):
        s3_client = self.session.client('s3')
        response = s3_client.list_buckets()
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')

    def upload_file(self, bucket_name, target_name):
        s3 = self.session.client('s3')
        with open(self.file_to_upload.name, "rb") as f:
            s3.upload_fileobj(f, bucket_name, target_name,
                              ExtraArgs={'ACL': 'public-read'})

    def download_file(self, bucket_name, file_to_get, save_as):
        s3 = self.session.client('s3')
        s3.download_file(bucket_name, file_to_get, save_as)

    def get_file(self):
        """Opens a file browser to select the text file to be used for TTS."""
        self.file_to_upload = filedialog.askopenfile(parent=window, mode='r', title='Choose a file')
        print(self.file_to_upload.name)


if __name__ == "__main__":
    aws_s3 = S3()
    window = tk.Tk()
    window.config(padx=30, pady=20)
    window.title("AWS S3 tool")
    select_region = tk.StringVar(window)
    select_region.set("eu-central-1")

    #Labels
    create_bucket = tk.Label(text="Create a new bucket:")
    create_bucket.grid(column=0, row=0, sticky="w")
    select_region_label = tk.Label(text="Select region:")
    select_region_label.grid(column=2, row=0, sticky="w")
    upload_file = tk.Label(text="Upload a file:")
    upload_file.grid(column=0, row=1, sticky="w")

    #Entries
    bucket_entry = tk.Entry(width=25)
    bucket_entry.grid(column=1, row=0, sticky="e")

    #Buttons
    upload_button = tk.Button(text="Select the file you want to upload", command=aws_s3.get_file)
    upload_button.grid(column=1, row=1, sticky="w")
    region_select_dropdown = tk.OptionMenu(window, select_region, *REGION_LIST)
    region_select_dropdown.grid(column=4, row=0, sticky="e")
    create_bucket_start = tk.Button(text="Start creation", command=aws_s3.create_bucket)
    create_bucket_start.grid(column=5, row=0, sticky="w")



#aws_s3.create_bucket(bucket_name="hulaspettest", region="eu-central-1")
    #aws_s3.list_buckets()
    #aws_s3.upload_file("hulaspettest",
    #                   "/Users/nbyy/Library/CloudStorage/OneDrive-Personal/Pictures/Screenshots/OculusScreenshot1610295573.jpeg",
    #                   "screenshot.jpeg")
    #aws_s3.download_file("hulaspettest", "screenshot.jpeg", "/Users/nbyy/Downloads/screenshot.jpeg")
    window.mainloop()