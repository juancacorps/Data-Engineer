from Google_Drive import upload_file
import os
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import unittest

URL = 'https://covid19.gob.gt/semaforo.html'
ID_FOLDER = 'ID of folder at Google Drive'
PATH = 'Your Path of folder'

class Download_xls_Test(unittest.TestCase):
    def setUp(self):
        self.profile = Options()
        profile = self.profile
        profile.set_preference("browser.download.dir", PATH)
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.driver = webdriver.Firefox(executable_path="./geckodriver",firefox_options=profile)
        driver = self.driver
        driver.maximize_window()
        ok = requests.get(URL)
        if ok.status_code == 200:
            driver.maximize_window()
            driver.get(URL)
        else:
            raise print('Page not available')

    def test_download_and_upload_xls(self):
        driver = self.driver
        button_download = driver.find_element_by_xpath('//div[@class="dt-button buttons-excel buttons-html5"]')
        button_download.click()
        sleep(25)
        try:
            FILES =  [file for _, _, files in os.walk(PATH) for file in files if 'Reporte_de_Covid' in file]
            PATH_FILE = f'{PATH}/{FILES[0]}'
            upload_file(PATH_FILE,ID_FOLDER) # Upload to Google Drive
        except Exception as e:
            print('*'*25)
            print(f'error at load file: {e}')
            print('*'*25)

    def test_delete_file_local(self):
        FILES =  [file for _, _, files in os.walk(PATH) for file in files if 'Reporte_de_Covid' in file]
        for file in FILES:
            os.remove(f'{PATH}/{file}')

    def tearDown(self):
        driver = self.driver
        driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)
