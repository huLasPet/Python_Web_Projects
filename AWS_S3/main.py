import logging
from boto3 import Session
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv


load_dotenv(r"/Users/nbyy/Library/CloudStorage/OneDrive-Personal/Python Round 2/IntelliJ/env")


class S3:
    def __init__(self):
        self.session = Session(aws_access_key_id=os.getenv("aws_s3_key"), aws_secret_access_key=os.getenv("aws_s3_secret"))

    def create_bucket(self, bucket_name, region=None):
        try:
            if region is None:
                s3_client = self.session.client('s3')
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client = self.session.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def list_buckets(self):
        s3_client = self.session.client('s3')
        response = s3_client.list_buckets()
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')

    def upload_file(self, bucket_name, source_file, target_name):
        s3 = self.session.client('s3')
        with open(source_file, "rb") as f:
            s3.upload_fileobj(f, bucket_name, target_name,
                              ExtraArgs={'ACL': 'public-read'})


if __name__ == "__main__":
    aws_s3 = S3()
    #aws_s3.create_bucket(bucket_name="hulaspettest", region="eu-central-1")
    #aws_s3.list_buckets()
    #aws_s3.upload_file("hulaspettest",
    #                   "/Users/nbyy/Library/CloudStorage/OneDrive-Personal/Pictures/Screenshots/OculusScreenshot1610295573.jpeg",
    #                   "screenshot.jpeg")
