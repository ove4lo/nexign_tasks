from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import requests

chrome_options = Options()

service = Service()

# Функция чтения терминов в файле
def load_terms(file_path="task3_folder/terms.txt"):
    with open(file_path, "r", encoding="utf-8") as file:
        return set(line.strip().lower() for line in file)  # Приводим все термины к нижнему регистру

# Функция проверки орфографии в тексте
def check_with_yandex_speller(text, it_terms):
    url = "https://speller.yandex.net/services/spellservice.json/checkText"
    MAX_LENGTH = 10000 # Ограничение на количество символов, так как нельзя передавать объемный текст
    chunks = [text[i:i+MAX_LENGTH] for i in range(0, len(text), MAX_LENGTH)] # Делим на части
    
    errors_set = set()
    try:
        for chunk in chunks:
            response = requests.post(url, data={"text": chunk})
            response.raise_for_status()
            errors = response.json()
            
            for error in errors:
                word = error['word'].strip()  # Убираем лишние пробелы
                
                # Если слово в списке терминов, пропускаем его
                if word.lower() in it_terms:
                    continue
                
                suggestions = ', '.join(error['s'])
                errors_set.add((word, suggestions))
        
        return list(errors_set)

    except requests.exceptions.RequestException as e:
        print(e)
        return []
    except requests.exceptions.JSONDecodeError:
        print("Ошибка")
        return []

# Загрузка списка IT-терминов
terms = load_terms()

# Функция для проверки орфографии на странице
def spelling(text, url_page):
    yandex_errors = check_with_yandex_speller(text, terms)
    
    if yandex_errors:
        # Читаем существующие данные из файла
        try:
            with open("task3_folder/errors.txt", "r", encoding="utf-8") as file:
                existing_data = file.read()
        except FileNotFoundError:
            existing_data = ""
        with open("task3_folder/errors.txt", "a", encoding="utf-8") as file:
            # проверка на существование записей для этой страницы, чтобы не произошло дублирования
            if f"ССЫЛКА НА СТРАНИЦУ САЙТА {url_page}:" not in existing_data:
                file.write(f"ССЫЛКА НА СТРАНИЦУ САЙТА {url_page}:\n")
                file.write("Ошибки:\n")
                for word, suggestions in yandex_errors:
                    file.write(f"Неверное слово: {word}\n")
                    corrected_word = ''.join(suggestions)
                    file.write(f"Варианты исправления: {corrected_word}\n\n")
                print(f"Ошибки слов на странице {url_page} записаны в файл 'errors.txt'")
            else:
                print(f"Ошибки для страницы {url_page} уже записаны в файл 'errors.txt'")
    else:
        print(f"Yandex Speller: ОШИБОК НЕТ на странице {url_page}")

# Функция проверки орфографии на всех страницах сайта
def task3(driver: webdriver.Chrome):
    try:
        driver.get("https://nexign.com/ru") 
                
        urls = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
        urls_href: list[str] = ["https://nexign.com/ru"]
        
        for url in urls:
            urls_href.append(url.get_attribute("href")) # Находим все ссылки 
        
        urls_href = list(set(urls_href)) # Избавляемся от дубликатов
        urls_href_copy = urls_href
        
        pattern = r"https:\/\/([a-zA-Z0-9-]+\.)?nexign\.com"
        # Убираем ссылки, которые ведут на сторонние сайты
        for url in urls_href_copy:
            if not re.match(pattern, url):
                urls_href.remove(url)
        
        for url in urls_href:
            driver.get(url) 
            text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text
            spelling(text, url)
                 
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        
if __name__ == "__main__":
    # Инициализация драйвера
    driver = webdriver.Chrome(service=service, options=chrome_options)
    task3(driver)
