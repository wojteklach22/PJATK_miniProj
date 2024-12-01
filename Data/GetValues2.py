from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

class GetValues2:
    def __init__(self):
        self.download_service = Service()
        self.driver = webdriver.Chrome(service=self.download_service)
        self.driver.get(r"https://zooexpress.pl/category/koty-i-kocieta-karmy-mokre?horizontal")

    def fetch_products(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'product_name'))
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'price'))
        )
        products_info = self.driver.find_elements(By.CLASS_NAME, 'product_name')
        prices_info = self.driver.find_elements(By.CLASS_NAME, 'price')

        page_data = []
        for name, price in zip(products_info, prices_info):
            if name.text and price.text:
                page_data.append({"name": name.text, "price": price.text})
        return page_data

    def fetch_all_products(self):
        products_data = self.fetch_products()
        number_of_pages = 18
        for page in range(2, number_of_pages + 1):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            btn_next_page = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'a[href="/category/koty-i-kocieta-karmy-mokre/{page}?horizontal"]')
                )
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn_next_page)
            btn_next_page.click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "product_name"))
            )
            products_data += self.fetch_products()

        return products_data

    def save_to_csv(self, products_data, filepath):
        with open(filepath, mode="w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "price"])
            writer.writeheader()
            writer.writerows(products_data)

    def close(self):
        self.driver.quit()
