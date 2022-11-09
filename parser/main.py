import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestClass:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def easy_download(self):
        self.driver.get('http://www.world-art.ru')
        _ = input()
        try:
            for i in self.driver.find_elements(By.XPATH, '//td[@class="review"]//label'):
                i.click()
        except Exception as e:
            print(e)


a = TestClass()
a.easy_download()
