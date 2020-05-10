import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

import config


def copy_or_paste(driver, btn: str):
    """You need to give 'c' letter or 'v' letter"""
    action = ActionChains(driver)
    action.key_down(Keys.CONTROL).send_keys(btn).key_up(Keys.CONTROL).perform()


def switch_tab(driver, tab_number):
    """Switch to a browser tab via tab_number"""
    tabs = driver.window_handles
    driver.switch_to.window(tabs[tab_number])


class ImageParser:
    """Parse image from the search system"""
    def __init__(self, word, driver):
        self.word = word
        self.driver = driver

    def find_word(self):
        """Open google and search the word"""
        self.driver.get(config.SEARCH_URL)
        search_input = self.driver.find_element_by_id('text')
        search_input.send_keys(self.word)
        search_input.send_keys(Keys.ENTER)

    def parse_image(self):
        """Search with find_word() and open google images and parse an image"""
        self.find_word()

        # Open images
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/nav/ul/li[2]/div[1]/a/span'
        ).click()
        switch_tab(self.driver, 1)

        # Get first image link
        image = self.driver.find_element_by_class_name('serp-item__link')
        image_src = image.get_attribute('href')

        # Copy an image to clipboard
        self.driver.get(image_src)
        self.driver.find_element_by_partial_link_text('Открыть').click()
        time.sleep(1)

        self.driver.find_element_by_xpath('/html/body/div[19]/div/div/div/div/div[3]/a[2]').click()
        switch_tab(self.driver, 2)

        time.sleep(2)
        copy_or_paste(self.driver, 'c')


class Translator:
    def __init__(self, word, driver):
        self.word = word
        self.driver = driver

    def get_translation(self):
        """Write to the translator the word and return its translation"""
        self.driver.get(config.TRANSLATOR_URL)
        self.driver.find_element_by_id('source').send_keys(self.word)
        time.sleep(1.5)

        translation = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]/span'
        ).text

        return translation


class VkManager:
    def __init__(self, word, driver):
        self.word = word
        self.driver = driver

    def vk_auth(self):
        """Open VK and auth to that"""
        self.driver.get(config.VK_PAGE)
        self.driver.find_element_by_id('quick_email').send_keys(config.VK_LOGIN)  # Login input
        self.driver.find_element_by_id('quick_pass').send_keys(config.VK_PASSWORD)  # Password input
        self.driver.find_element_by_id('quick_login_button').click()  # Submit button
        time.sleep(3)

    def send_message(self, translation):
        """Auth with vk_auth() and send the word, the translation + the copied image to your chat"""
        self.vk_auth()

        # Open chat and write the word + its translation and parsed image
        self.driver.get(config.VK_CHAT_URL)
        self.driver.find_element_by_xpath('//*[@id="im_editable474106968"]').send_keys(
            f'{self.word} - {translation}'
        )
        copy_or_paste(self.driver, 'v')
        time.sleep(3)

        # Send a message
        self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div[4]/div[1]/button'
        ).click()


def main():
    """Define driver and word.
    Activate methods to parse, translate and send a message
    """
    driver = webdriver.Chrome(r'C:\Users\user\Documents\chromedriver.exe')
    driver.maximize_window()
    word = input('Write a word that you wanna remember\n> ')

    image_parser = ImageParser(word, driver)
    vk_manager = VkManager(word, driver)
    translator = Translator(word, driver)

    # Parse image, get translation, send message
    image_parser.parse_image()
    translation = translator.get_translation()
    vk_manager.send_message(translation)

    time.sleep(1.5)
    driver.close()


if __name__ == '__main__':
    main()
