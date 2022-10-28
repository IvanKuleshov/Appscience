import boto3
import os

os.environ['S3_BUCKET'] = 'secret'
os.environ['S3_FILE_PATH'] = 'secret'
os.environ['S3_ACCESS_KEY_ID'] = 'secret'
os.environ['S3_SECRET_ACCESS_KEY'] = 'secret'


def upload_parse_result(file_name):
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    """
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.environ["S3_ACCESS_KEY_ID"],
                             aws_secret_access_key=os.environ["S3_SECRET_ACCESS_KEY"],
                             )
    s3_client.upload_file(file_name, os.environ["S3_BUCKET"], os.environ["S3_FILE_PATH"])


upload_parse_result("Appscience_parcing_Kuleshov.csv")