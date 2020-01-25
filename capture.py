import os
from datetime import datetime
from urllib.parse import urlparse
import configparser
import argparse
import boto3
import logging
from botocore.exceptions import ClientError
from selenium import webdriver

logger = logging.getLogger('capture_pages')


def init_logger():
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)


def handle_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='url')
    parser.add_argument('-f', '--full-screenshot', action='store_true', help='enable to take a full screenshot')
    parser.add_argument('-l', '--location', default=False, help='enable to change saving location')
    parser.add_argument('-s3', '--s3', action='store_true', default=False, help='enable to save to s3')

    return parser.parse_args()


def load_config():
    config = configparser.ConfigParser()
    config.read('capture-pages.ini')
    return config


def start_selenium_driver(url):
    logger.info('Creating Selenium web driver...')
    options = webdriver.ChromeOptions()
    options.headless = True

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    return driver


def set_full_screen(driver):
    total_width = driver.execute_script('return screen.width')
    total_height = driver.execute_script('return document.body.scrollHeight')
    driver.set_window_size(total_width, total_height)


def format_screenshot_name(url):
    website_name = urlparse(url).netloc.split('.')[0]
    return website_name + datetime.now().strftime('%m%d%y%H%M%S')


def upload_to_s3(file_name, bucket, aws_access_key_id, aws_secret_access_key):
    logger.info('Trying to connect to S3...')
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    object_name = os.path.basename(file_name)
    s3_client.upload_file(file_name, bucket, object_name)
    logger.info('Uploaded to S3 successfully.')


def main():
    init_logger()
    args = handle_arguments()

    location = 'screenshots' if not args.location else args.location
    if not os.path.isdir(location):
        try:
            os.makedirs(location)
        except OSError:
            logger.fatal('', exc_info=True)

    url = args.url
    driver = None
    try:
        driver = start_selenium_driver(url)
    except:
        logger.fatal('Failed to initialize Selenium web driver.', exc_info=True)

    if args.full_screenshot:
        set_full_screen(driver)

    screenshot_path = '{}.png'.format(os.path.join(location, format_screenshot_name(url)))

    logger.info('Taking a screenshot.')
    driver.find_element_by_tag_name('body') \
        .screenshot(screenshot_path)
    logger.info('Saved screenshot to \'{}\'.'.format(screenshot_path))

    if args.s3:
        config = load_config()
        if 'AWS' not in config:
            logger.fatal('No AWS section found in config file.')

        aws_config = config['AWS']

        if 'Bucket' not in aws_config or 'AWSAccessKeyId' not in aws_config or 'AWSSecretAccessKey' not in aws_config:
            logger.fatal('No AWS parameters found in config file.')

        try:
            upload_to_s3(screenshot_path, aws_config['Bucket'], aws_config['AWSAccessKeyId'],
                         aws_config['AWSSecretAccessKey'])
        except ClientError:
            logger.exception('Failed to upload file to S3.')

    driver.quit()
    logger.info('Done!')


if __name__ == '__main__':
    main()
