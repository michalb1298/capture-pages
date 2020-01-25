import logging

from selenium import webdriver

logger = logging.getLogger(__name__)


def init_selenium_driver():
    logger.info('Initializing Selenium web driver...')
    options = webdriver.ChromeOptions()
    options.headless = True

    driver = webdriver.Chrome(options=options)
    return driver


def set_driver_full_screen(driver):
    total_width = driver.execute_script('return screen.width')
    total_height = driver.execute_script('return document.body.scrollHeight')
    driver.set_window_size(total_width, total_height)


def capture_web_page(url, screenshot_path, full_screenshot=False):
    driver = init_selenium_driver()
    try:
        driver.get(url)

        if full_screenshot:
            set_driver_full_screen(driver)

        logger.info('Taking a screenshot.')
        driver.find_element_by_tag_name('body') \
            .screenshot(screenshot_path)
        logger.info('Saved screenshot to \'{}\'.'.format(screenshot_path))
    finally:
        driver.quit()

