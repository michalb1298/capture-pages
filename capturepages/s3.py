import logging

import boto3

logger = logging.getLogger(__name__)


def upload_file_to_s3(file_name, object_name, bucket, aws_access_key_id, aws_secret_access_key):
    logger.info('Trying to connect to S3...')
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    s3_client.upload_file(file_name, bucket, object_name)
    logger.info('Uploaded to S3 successfully.')
