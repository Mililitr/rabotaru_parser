import time
import pickle
import signal
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Флаг для остановки цикла
stop_flag = False

def signal_handler(sig, frame):
    global stop_flag
    stop_flag = True

# Назначим обработчик сигнала SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

# создаем драйвер
driver = webdriver.Chrome()

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)

driver.get("https://www.rabota.ru/v3_searchResumeByParamsResults.html")

# загрузка куки
with open("cookies.pkl", "rb") as file:
    cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)
driver.refresh()

# сохранение куки
with open("cookies.pkl", "wb") as file:
    pickle.dump(driver.get_cookies(), file)

# область
driver.get("https://adygeya.rabota.ru/v3_searchResumeByParamsResults.html")

#возраст и профессии
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
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input.keywords-input"))
).send_keys("оператор колл-центра, оператор контакт центра, Оператор входящей связь, диспетчер на телефоне, продавец, администратор, официант, бармен, секретарь, помощник руковдителя")
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input.blue_btn.expanded-search-btn"))
).click()

index = 1
candidate_dict = {}
candidate_name = None
contact_info = None
while True:
    if stop_flag:
        break

    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"div.resum_rez_item[data-position='{index}']"))
        )
        element.click()

        driver.execute_script("arguments[0].scrollIntoView();", element)
    
        try:
            WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.button_show_contacts.blue_btn.blue_btn_res-card.mt_10"))
            ).click()
            WebDriverWait(driver, 4).until(EC.alert_is_present()).accept()
        except: 
            pass

        try:
            candidate_name = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.candidate-name"))
            ).text
            try:
                WebDriverWait(driver, 4).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.js-xxx-phone.fw-normal"))
                ).click()
            except: 
                pass
            contact_info = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.t_14.mt_15.email-phone.js-resume-contacts"))
            ).text

            # добавление кандидата в словарь
            if candidate_name not in candidate_dict:
                candidate_dict[candidate_name] = contact_info
                index += 1
        except: 
            index += 1
    except: 
        index += 1
    
    if index == 1000:
        break

# Сохранение данных в Excel
df = pd.DataFrame(list(candidate_dict.items()), columns=['Candidate Name', 'Contact Info'])
df.to_excel('candidates.xlsx', index=False)

driver.quit()

# # логин
# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.NAME, "login"))
# ).send_keys("115@skewes.ru")
# driver.find_element(By.CSS_SELECTOR, "button[aria-label='Продолжить']").click()

# # пароль
# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.NAME, "password"))
# ).send_keys("m5kGdQwl")
# driver.find_element(By.CSS_SELECTOR, "button[aria-label='Продолжить']").click()