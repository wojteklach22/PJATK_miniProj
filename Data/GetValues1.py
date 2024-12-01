from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

class GetValues1:
    def __init__(self):
        self.download_service = Service()
        self.driver = webdriver.Chrome(service=self.download_service)
        self.driver.get(r"https://zookarina.pl/pol_m_Koty_Karma-i-przysmaki_Karma-mokra-1984.html")
        self.accept_cookies()

    def accept_cookies(self):
        btn_allow = self.driver.find_element("css selector", "a.acceptAll.btn.--solid.--large")
        btn_allow.click()

    def fetch_products(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'product__name'))
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.product__prices strong.price.--main'))
        )
        products_info = self.driver.find_elements(By.CLASS_NAME, 'product__name')
        prices_info = self.driver.find_elements(By.CSS_SELECTOR, '.product__prices strong.price.--main')

        page_data = []
        for name, price in zip(products_info, prices_info):
            if name.text and price.text:
                page_data.append({"name": name.text, "price": price.text})
        return page_data

    def fetch_all_products(self):
        products_data = self.fetch_products()

        btn_2nd_page = self.driver.find_element(By.CSS_SELECTOR, "li.pagination__element.--item a.pagination__link")
        btn_2nd_page.click()
        time.sleep(7) # Need this sleep because website is loading extremly slowly
        products_data += self.fetch_products()

        return products_data

    def save_to_csv(self, products_data, filepath):
        with open(filepath, mode="w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "price"])
            writer.writeheader()
            writer.writerows(products_data)

    def close(self):
        self.driver.quit()
