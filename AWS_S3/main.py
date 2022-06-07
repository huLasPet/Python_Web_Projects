import logging
from boto3 import Session
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
from tkinter import filedialog, ttk
import tkinter as tk



load_dotenv(r"/Users/nbyy/Library/CloudStorage/OneDrive-Personal/Python Round 2/IntelliJ/env")
REGION_LIST = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-central-1"]

def on_tab_change(event):
    tab = event.widget.tab('current')['text']
    if tab == 'Download file':
        aws_s3.list_buckets(tab3)
    elif tab == 'Upload file':
        aws_s3.list_buckets(tab2)
    elif tab == "Delete object":
        aws_s3.list_buckets(tab4)


class S3:
    def __init__(self):
        self.existing_buckets = []
        self.uploaded_files = []
        self.file_to_upload = None
        self.download_path = None
        self.session = Session(aws_access_key_id=os.getenv("aws_s3_key"), aws_secret_access_key=os.getenv("aws_s3_secret"))
        self.s3_client = self.session.client('s3')

    def create_bucket(self):
        try:
            self.s3_client = self.session.client('s3', region_name=select_region.get())
            location = {'LocationConstraint': select_region.get()}
            self.s3_client.create_bucket(Bucket=bucket_entry.get(),
                                        CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            bucket_status = tk.Label(text=e.response["Error"]["Code"])
            bucket_status.grid(column=6, row=0, sticky="w")
            return False
        bucket_status = tk.Label(tab1,text="Creation successful")
        bucket_status.grid(column=5, row=0, sticky="w")
        return True

    def list_buckets(self, tab):
        response = self.s3_client.list_buckets()
        self.existing_buckets.clear()
        for bucket in response['Buckets']:
            self.existing_buckets.append(bucket["Name"])
        select_bucket_dropdown = tk.OptionMenu(tab, select_bucket, *aws_s3.existing_buckets)
        select_bucket_dropdown.grid(column=1, row=0, sticky="w")

    def upload_file(self):
        with open(self.file_to_upload.name, "rb") as f:
            self.s3_client.upload_fileobj(f, select_bucket.get(), uploaded_file_name.get(),
                              ExtraArgs={'ACL': 'public-read'})
        upload_status = tk.Label(tab2, text="Upload complete")
        upload_status.grid(column=2, row=1, sticky="w")

    def download_file(self):
        self.download_path = filedialog.asksaveasfile(parent=window, mode='w', title="Save to")
        self.s3_client.bucket_file(select_bucket.get(), bucket_file.get(), self.download_path.name)
        download_status = tk.Label(tab3, text="Download complete")
        download_status.grid(column=2, row=1, sticky="w")
        
    def delete_object(self):
        self.s3_client.delete_object(Bucket=select_bucket.get(), Key=bucket_file.get())

    def get_file(self):
        """Opens a file browser to select the file to upload."""
        self.file_to_upload = filedialog.askopenfile(parent=window, mode='r', title='Choose a file')


    def list_bucket_objects(self, tab):
        bucket = select_bucket.get()
        if bucket == "":
            missing_selection = tk.Label(tab3, text="Select a bucket first.")
            missing_selection.grid(column=3, row=0, sticky="w")
        else:
            listed_objects = self.s3_client.list_objects_v2(Bucket=select_bucket.get())
            self.uploaded_files.clear()
            for object in listed_objects["Contents"]:
                self.uploaded_files.append(object["Key"])
            self.bucket_file_dropdown = tk.OptionMenu(tab, bucket_file, *aws_s3.uploaded_files)
            self.bucket_file_dropdown.grid(column=1, row=1, sticky="w")


if __name__ == "__main__":
    aws_s3 = S3()
    window = tk.Tk()
    window.title("AWS S3 tool")
    tabControl = ttk.Notebook(window)
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)
    tab4 = ttk.Frame(tabControl)
    tab5 = ttk.Frame(tabControl)
    tabControl.add(tab1, text='Create bucket')
    tabControl.add(tab2, text='Upload file')
    tabControl.add(tab3, text='Download file')
    tabControl.add(tab4, text='Delete object')
    tabControl.add(tab5, text='Delete bucket')
    tabControl.pack(expand=1, fill="both")

#Dropdown initial
    select_region = tk.StringVar(window)
    select_region.set("eu-central-1")
    select_bucket = tk.StringVar(window)
    bucket_file = tk.StringVar(window)

#Labels
#Tab1
    bucket_name_label = tk.Label(tab1, text="Name of the bucket:")
    bucket_name_label.grid(column=0, row=0)
    select_region_label = tk.Label(tab1, text="Select region:")
    select_region_label.grid(column=0, row=1, sticky="w")
#Tab2
    upload_file = tk.Label(tab2, text="Upload a file:")
    upload_file.grid(column=0, row=1, sticky="w")
    upload_bucket_select = tk.Label(tab2, text="Select a bucket to upload to:")
    upload_bucket_select.grid(column=0, row=0, sticky="w")
    uploaded_file_name_label = tk.Label(tab2, text="Object name in the bucket, with extension:")
    uploaded_file_name_label.grid(column=0, row=2, sticky="w")
#Tab3
    download_file_label = tk.Label(tab3, text="Select a file to download:")
    download_file_label.grid(column=0, row=1, sticky="w")
    download_bucket_select = tk.Label(tab3, text="Select a bucket to download from:")
    download_bucket_select.grid(column=0, row=0, sticky="w")
#Tab4
    delete_file_label = tk.Label(tab4, text="Select a file to delete:")
    delete_file_label.grid(column=0, row=1, sticky="w")
    download_bucket_select = tk.Label(tab4, text="Select a bucket to delete from:")
    download_bucket_select.grid(column=0, row=0, sticky="w")



#Entries
#Tab1
    bucket_entry = tk.Entry(tab1, width=25)
    bucket_entry.grid(column=1, row=0, sticky="w")
#Tab2
    uploaded_file_name = tk.Entry(tab2, width=12)
    uploaded_file_name.grid(column=1, row=2, sticky="w")
#Tab3



#Buttons
#Tab1
    region_select_dropdown = tk.OptionMenu(tab1, select_region, *REGION_LIST)
    region_select_dropdown.grid(column=1, row=1, sticky="w")
    create_bucket_start = tk.Button(tab1, text="Start creation", command=aws_s3.create_bucket)
    create_bucket_start.grid(column=2, row=3, sticky="w")
#Tab2
    upload_button = tk.Button(tab2, text="Select file", command=aws_s3.get_file)
    upload_button.grid(column=1, row=1, sticky="w")
    upload_file_start = tk.Button(tab2, text="Start upload", command=aws_s3.upload_file)
    upload_file_start.grid(column=2, row=3, sticky="w")
#Tab3
    get_files_button = tk.Button(tab3, text="Get file list", command=lambda: aws_s3.list_bucket_objects(tab3))
    get_files_button.grid(column=2, row=0, sticky="w")
    download_start_button = tk.Button(tab3, text="Download", command=aws_s3.download_file)
    download_start_button.grid(column=3, row=3, sticky="w")
#Tab4
    get_delete_files_button = tk.Button(tab4, text="Get file list", command=lambda: aws_s3.list_bucket_objects(tab4))
    get_delete_files_button.grid(column=2, row=0, sticky="w")
    delete_start_button = tk.Button(tab4, text="Delete object", command=aws_s3.delete_object)
    delete_start_button.grid(column=3, row=3, sticky="w")




    tabControl.bind('<<NotebookTabChanged>>', on_tab_change)
    window.mainloop()