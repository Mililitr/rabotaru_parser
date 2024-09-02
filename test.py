import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройки для Chrome
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')

# Создание драйвера
driver = webdriver.Chrome(options=options)

# Переход на страницу и загрузка куки
driver.get("https://www.rabota.ru/v3_searchResumeByParamsResults.html")

try:
    with open("cookies.pkl", "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()
except FileNotFoundError:
    print("Файл cookies.pkl не найден. Продолжение без загрузки куков.")

# Переход на нужную страницу
driver.get("https://adygeya.rabota.ru/v3_searchResumeByParamsResults.html")

# Установка возраста
try:
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.js-extended-search-link.red_text.t_14"))
    ).click()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.js-age-from.b-text-input.b-short-txtinput"))
    ).send_keys("18")
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.js-age-to.b-text-input.b-short-txtinput"))
    ).send_keys("47")
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.blue_btn.expanded-search-btn"))
    ).click()
except Exception as e:
    print(f"Ошибка при установке возраста: {e}")

visited_class = "box-wrapper__resume-name_visited"
previous_count = 0

while True:
    try:
        # Получаем все элементы
        all_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.resum_rez_item"))
        )

        # Проверяем, есть ли элементы без класса visited_class
        unvisited_items = [item for item in all_items if visited_class not in item.get_attribute("class")]

        if not unvisited_items and len(all_items) > previous_count:
            # Если все элементы посещены, скроллим вниз до последнего элемента
            driver.execute_script("arguments[0].scrollIntoView();", all_items[-1])
            time.sleep(2)  # Небольшая задержка для загрузки новых элементов
            previous_count = len(all_items)
        elif not unvisited_items:
            # Если все элементы посещены и новые не загружаются, выходим из цикла
            print("Все элементы были посещены.")
            break
        else:
            # Обрабатываем только непосещенные элементы
            for item in unvisited_items:
                driver.execute_script("arguments[0].scrollIntoView();", item)
                driver.execute_script("arguments[0].click();", item)
                
                try:
                    WebDriverWait(driver, 4).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.button_show_contacts.blue_btn.blue_btn_res-card.mt_10"))
                    ).click()
                    WebDriverWait(driver, 4).until(EC.alert_is_present()).accept()
                except Exception as e:
                    print(f"Ошибка при получении контактов: {e}")

                try:
                    candidate_name = WebDriverWait(driver, 4).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "p.candidate-name"))
                    ).text
                    try:
                        WebDriverWait(driver, 4).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.js-xxx-phone.fw-normal"))
                        ).click()
                    except Exception as e:
                        print(f"Ошибка при клике на телефон: {e}")
                    contact_info = WebDriverWait(driver, 4).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.t_14.mt_15.email-phone.js-resume-contacts"))
                    ).text
                    print("Candidate Name:", candidate_name)
                    print("Contact Info:", contact_info)
                except Exception as e:
                    print(f"Ошибка при получении информации о кандидате: {e}")

            # Обновляем предыдущий счетчик
            previous_count = len(all_items)

    except Exception as e:
        print(f"Ошибка при получении элементов: {e}")
        break

driver.quit()