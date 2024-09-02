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



# парсер
driver.get("https://adygeya.rabota.ru/v3_searchResumeByParamsResults.html")

#возраст
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

#резюме
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.b-center__box.resum_rez_item.resum_rez_active"))
).click()
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.button_show_contacts.blue_btn.blue_btn_res-card.mt_10"))
).click()
WebDriverWait(driver, 10).until(EC.alert_is_present()).accept()

# контакты
candidate_name = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "p.candidate-name"))
).text
contact_info = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.t_14.mt_15.email-phone.js-resume-contacts"))
).text

print("Candidate Name:", candidate_name)
print("Contact Info:", contact_info)

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