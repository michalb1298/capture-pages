import sys
import os
from datetime import datetime
from urllib.parse import urlparse

import argparse
from selenium import webdriver


def handle_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='url')

    return parser.parse_args()


def start_selenium_driver(url):
    options = webdriver.ChromeOptions()
    options.headless = True

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    return driver


def format_screenshot_name(url):
    website_name = urlparse(url).netloc.split('.')[0]
    return website_name + datetime.now().strftime('%m%d%y%H%M%S')


def main():
    args = handle_arguments()

    url = args.url
    driver = start_selenium_driver(url)

    if not os.path.isdir('screenshots'):
        os.makedirs('screenshots')

    driver.find_element_by_tag_name('body')\
        .screenshot('screenshots/{}.png'.format(format_screenshot_name(url)))


if __name__ == '__main__':
    main()
