from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.firefox.options import Options
# Imported due to running browser in headless mode (in the background).

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# Imported due to method 'presence_of_element_located' (and possibly other useful methods).

import sys
import time
import os
import re
import requests


def already_stored_images():
    """
    It check images which are already stored in current working directory.
    The purpose of this method is to prevent saving already stored images.
    :return: List of images (jpeg, jpg, png) names.
    """

    # It checks current working directory (without nested components).
    stored_files = [file for file in os.listdir(os.getcwd()) if os.path.isfile(file)]

    image_extensions = ['.jpeg', '.jpg', '.png']

    stored_images = []

    for stored_file in stored_files:
        # Splitting path to list by name and extension.
        # Accessing extension only with [1].
        if os.path.splitext(stored_file)[1] in image_extensions:
            stored_images.append(stored_file)

    return stored_images


def browser_setup(executable_path_p, user_argument_p):
    """
    It setups the browser in headless mode (background mode).
    :param executable_path_p: Path to Firefox browser driver.
    :param user_argument_p: User provides URL as argument to profile on website 'https://www.lide.cz/'.
    :return: Instance of browser.
    """

    # To make browser run in the background.
    options = Options()
    options.headless = True

    browser_init = webdriver.Firefox(options=options, executable_path=executable_path_p)

    browser_init.get(user_argument_p)
    browser_init.maximize_window()
    browser_init.implicitly_wait(10)

    print('Info: Browser initialized.')

    return browser_init


def load_more(browser_p):
    """
    It searches for Load more button and clicks it until it is not available. At this point, dynamic website is loaded.
    Then it saves all profile images with same URL names. They are saved in same location as the script.
    If any image is already saved in the same location, it will not be saved.
    Also, console displays informative messages of what is currently happening.
    :param browser_p: Instance of browser.
    """

    try:

        while WebDriverWait(browser_p, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'next-photos'))):

            # Getting inner text of span element using the 'innerText' argument.
            load_more_button = browser_p.find_element_by_class_name(
                'next-photos'
            ).find_elements_by_tag_name(
                'span'
            )[0].get_attribute('innerText')

            print('Info: Button "' + load_more_button + '" is available.')
            time.sleep(5)

            browser_p.find_element_by_class_name('next-photos').find_elements_by_tag_name('span')[0].click()
            # Option below would be also possible.
            # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'next-photos'))).click()

            print('Event: Button clicked.')
            time.sleep(5)

        time.sleep(5)

    except (NoSuchElementException, TimeoutException):
        print('Info: Load more button is not (no longer) available.')


def save_images(browser_p, saved_images_count_p, stored_images_count_p):
    """
    It saves the profile images.
    Method 'already_stored_images' is used.
    :param browser_p: Instance of browser.
    :param saved_images_count_p: Count of saved images from the profile.
    :param stored_images_count_p: Count of skipped images from the profile.
    """

    for image in browser_p.find_elements_by_xpath('//div[@class="imageBox"]/img'):

        image_url = image.get_attribute('src')

        request_image = requests.get(image_url)
        request_image.raise_for_status()

        image_url_basename = os.path.basename(image_url)
        image_name = re.sub(r'\?.*', '', image_url_basename)

        # Using already_stored_images().
        if image_name not in already_stored_images():

            image_file = open(image_name, 'wb')

            for chunk in request_image.iter_content(100000):
                image_file.write(chunk)

            image_file.close()

            print('Info: ' + image_name + ' downloaded.')
            saved_images_count_p += 1

        else:
            print('Info: ' + image_name + ' skipped (already stored).')
            stored_images_count_p += 1


if __name__ == '__main__':
    """
    User can provide only 1 argument (website profile) at a time.
    """

    firefox_executable_path = r'c:\Firefox_GeckoDriver_Win64\geckodriver.exe'

    if len(sys.argv) == 2:

        saved_images_count = 0
        skipped_images_count = 0

        user_argument = sys.argv[1]

        try:

            browser = browser_setup(firefox_executable_path, user_argument)

            load_more(browser)
            save_images(browser, saved_images_count, skipped_images_count)

            browser.close()
            browser.quit()

            print()
            print('Info: Count of saved images: ' + str(saved_images_count))
            if saved_images_count == 0:
                print('Info: There are no images on the profile.')
            else:
                print('Info: Count of skipped images: ' + str(skipped_images_count))

        except InvalidArgumentException:
            print('Info: URL is not valid.')

    else:
        print('Info: Wrong amount of URL(s) provided as argument(s). Only 1 argument has to be given.')

