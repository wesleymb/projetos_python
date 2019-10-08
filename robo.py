# -*- coding: utf-8 -*-
import time
import os


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



path_chromedriver = os.path.join(os.environ['USERPROFILE'], 'Desktop','ajuda_o_ze','chromedriver.exe')
path_download = os.path.join(os.environ['USERPROFILE'], 'Desktop','ajuda_o_ze','download')

options = Options()
options.add_experimental_option("prefs", {"download.default_directory": path_download})


def abrir_site():

    driver = webdriver.Chrome(executable_path=path_chromedriver, chrome_options=options)
    driver.get('https://www.globo.com/')




if __name__ == '__main__':
    abrir_site()