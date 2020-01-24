import os
from datetime import datetime
from urllib.parse import urlparse
import configparser
import argparse
import boto3
from selenium import webdriver


def handle_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='url')
    parser.add_argument('-f', '--full-screenshot', action='store_true', help='enable to take a full screenshot')
    parser.add_argument('-l', '--location', default=False, help='enable to change saving location')
    parser.add_argument('-s3', '--s3', action='store_true', default=False, help='enable to save to s3')

    return parser.parse_args()


def handle_configuration():
    config = configparser.ConfigParser()
    config.read('capture-pages.ini')
    return config


def start_selenium_driver(url):
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
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    object_name = os.path.basename(file_name)
    s3_client.upload_file(file_name, bucket, object_name)


def main():
    args = handle_arguments()

    location = 'screenshots' if not args.location else args.location
    if not os.path.isdir(location):
        os.makedirs(location)

    url = args.url
    driver = start_selenium_driver(url)

    if args.full_screenshot:
        set_full_screen(driver)

    screenshot_path = '{}.png'.format(os.path.join(location, format_screenshot_name(url)))

    driver.find_element_by_tag_name('body') \
        .screenshot(screenshot_path)

    if args.s3:
        aws_config = handle_configuration()['AWS']
        upload_to_s3(screenshot_path, aws_config['Bucket'], aws_config['AWSAccessKeyId'],
                     aws_config['AWSSecretAccessKey'])

    driver.quit()


if __name__ == '__main__':
    main()
