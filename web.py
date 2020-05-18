import os
import numpy as np
from selenium import webdriver


# uses chrome driver to scrape a random puzzle from https://www.websudoku.com/
def web_download():
    try:
        # creates new webdriver
        chrome_options = webdriver.ChromeOptions()
        # makes sure webdriver is named CHROME
        driver_name = 'CHROME'
        path_to_chrome_driver = os.environ[driver_name].replace('\\', '//')
        # create browser
        browser = webdriver.Chrome(executable_path=path_to_chrome_driver, chrome_options=chrome_options)
        # open URL
        browser.get('https://www.websudoku.com/')
        # scrapes puzzle from website
        frame = browser.find_element_by_xpath('.//frame')
        browser.switch_to.frame(frame)
        table = browser.find_element_by_xpath('.//table[@id="puzzle_grid"]')
        given = np.empty((9, 9), dtype=int)
        trs = table.find_elements_by_xpath('.//tr')
        r = 0
        for tr in trs:
            tds = tr.find_elements_by_xpath(".//td")
            c = 0
            for td in tds:
                ipt = td.find_element_by_xpath(".//input").get_attribute('value')
                given[r, c] = 0 if ipt == '' else int(ipt)
                c += 1
            r += 1
        # quit the browser
        browser.quit()
        return given
    except:
        return None