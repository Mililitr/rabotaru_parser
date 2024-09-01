import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# создаем драйвер
driver = webdriver.Chrome()
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

# ожидание резюме
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.b-center__box.resum_rez_item.resum_rez_active"))
).click()

# парсер


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

time.sleep(10000)