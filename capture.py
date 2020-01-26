import argparse
import configparser
import logging
import os
import sys
from datetime import datetime
from urllib.parse import urlparse
from boto3.exceptions import Boto3Error
from botocore.exceptions import BotoCoreError
from selenium.common.exceptions import WebDriverException

from capturepages import capture_web_page, upload_file_to_s3

logger = logging.getLogger('capturepages')


def init_logger():
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-f', '--full-screenshot', action='store_true', help='take a full screenshot')
    parser.add_argument('-l', '--location', default='screenshots',
                        help='path to save screenshot, default: screenshots')
    parser.add_argument('-s3', action='store_true', default=False,
                        help='save to s3, requires configuration file')

    return parser.parse_args()


def load_config():
    config = configparser.ConfigParser()
    config.read('capture-pages.ini')
    return config


def format_screenshot_name(url, extension='png'):
    website_name = urlparse(url).netloc.split('.')[0]
    date_string = datetime.now().strftime('%m%d%y%H%M%S')
    return f'{website_name}{date_string}.{extension}'


def get_aws_config():
    config = load_config()
    if 'AWS' not in config:
        logger.fatal('No AWS section found in config file.')
    aws_config = config['AWS']
    if 'Bucket' not in aws_config or 'AWSAccessKeyId' not in aws_config or 'AWSSecretAccessKey' not in aws_config:
        logger.fatal('No AWS parameters found in config file.')
    return aws_config['Bucket'], aws_config['AWSAccessKeyId'], aws_config['AWSSecretAccessKey']


def main():
    init_logger()
    args = parse_arguments()

    screenshots_directory = args.location
    if not os.path.isdir(screenshots_directory):
        try:
            os.mkdir(screenshots_directory)
        except OSError:
            logger.exception(f'Failed to create screenshots directory: {screenshots_directory}.')
            sys.exit()

    screenshot_file_name = format_screenshot_name(args.url)
    screenshot_path = os.path.join(screenshots_directory, screenshot_file_name)
    try:
        capture_web_page(args.url, screenshot_path, args.full_screenshot)
    except WebDriverException:
        logger.exception('Couldn\'t capture web page.')
        sys.exit()

    if args.s3:
        bucket, aws_access_key_id, aws_secret_access_key = get_aws_config()

        try:
            upload_file_to_s3(screenshot_path, screenshot_file_name, bucket, aws_access_key_id,
                              aws_secret_access_key)
        except (BotoCoreError, Boto3Error):
            logger.exception('Failed to upload file to S3.')

    logger.info('Done!')


if __name__ == '__main__':
    main()
