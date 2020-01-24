import os
from datetime import datetime
from urllib.parse import urlparse

import argparse
from selenium import webdriver


def handle_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='url')
    parser.add_argument('-f', '--full-screenshot', action='store_true', help='enable to take a full screenshot')
    parser.add_argument('-l', '--location', default=False, help='enable to change saving location')

    return parser.parse_args()


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


def main():
    args = handle_arguments()

    location = 'screenshots' if not args.location else args.location
    if not os.path.isdir(location):
        os.makedirs(location)

    url = args.url
    driver = start_selenium_driver(url)

    if args.full_screenshot:
        set_full_screen(driver)

    driver.find_element_by_tag_name('body')\
        .screenshot('{}/{}.png'.format(location, format_screenshot_name(url)))

    driver.quit()


if __name__ == '__main__':
    main()
