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

# Функция поиска слова "Nexign"
def task2(driver: webdriver.Chrome):
    try:
        driver.get("https://nexign.com/ru") 
        
        word = "Nexign"
        text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text.lower()
        
        # Подсчет слов в тексте
        nexign_counts = text.count(word.lower())
        
        print(nexign_counts)
        
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        
if __name__ == "__main__":
    # Инициализация драйвера
    driver = webdriver.Chrome(service=service, options=chrome_options)
    task2(driver)
