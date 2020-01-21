import sys
import os
from urllib.parse import urlparse
from selenium import webdriver


def start_selenium_driver(url):
    options = webdriver.ChromeOptions()
    options.headless = True

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    return driver


def main():
    if len(sys.argv) == 1:
        print("usage: capture.py <url>")

    else:
        url = sys.argv[1]
        driver = start_selenium_driver(url)
        if not os.path.isdir("screenshots"):
            os.makedirs("screenshots")
        driver.find_element_by_tag_name('body')\
            .screenshot('screenshots/{}.png'.format(urlparse(url).netloc))


if __name__ == '__main__':
    main()
