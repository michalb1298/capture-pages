import logging
from screeninfo import get_monitors
from selenium import webdriver

logger = logging.getLogger(__name__)


def init_selenium_driver():
    logger.info('Initializing Selenium web driver...')
    options = webdriver.ChromeOptions()
    options.headless = True

    driver = webdriver.Chrome(options=options)

    screen_dimensions = get_monitors()[0]
    screen_width = screen_dimensions.width
    screen_height = screen_dimensions.height
    driver.set_window_size(screen_width, screen_height)

    return driver


def set_driver_full_screen(driver):
    screen_width = driver.get_window_size()['width']
    total_height = driver.execute_script('return document.body.scrollHeight')
    driver.set_window_size(screen_width, total_height)


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

