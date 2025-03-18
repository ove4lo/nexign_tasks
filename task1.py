from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()

service = Service()

# Функция автокликов
def task1(driver: webdriver.Chrome):
    try:
        driver.get("https://nexign.com/ru") 
        
        # Нажатие на "Продукты и решения"
        navbar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "menu-new")))
        navbar_buttons = navbar.find_elements(By.TAG_NAME, "li")
        navbar_buttons[0].click()
        
        # Нажатие на "Инструменты для ИТ-команд"
        navbar_background = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "menu-new")))
        navbar_background_buttons = navbar_background.find_elements(By.CLASS_NAME, "menu-double-column")
        navbar_background_buttons[3].click()
        
        # Нажатие на "Nexign Nord"
        columns = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "menu-column-one")))
        rows = columns[3].find_elements(By.TAG_NAME, "li")
        row_button = rows[1].find_element(By.TAG_NAME, "a")
        row_button.click()
        
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        
if __name__ == "__main__":
    # Инициализация драйвера
    driver = webdriver.Chrome(service=service, options=chrome_options)
    task1(driver)
