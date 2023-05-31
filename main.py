from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

chrome_web_driver = "C:\development\chromedriver_win32"
s = Service(chrome_web_driver)
driver = webdriver.Chrome(service=s)

driver.get("http://orteil.dashnet.org/experiments/cookie/")
cookie_img = driver.find_element(By.ID, "cookie")
ids = driver.find_elements(By.CSS_SELECTOR, "#store div")
ids_list = []
for id in ids:
    ids_list.append(id.get_attribute("id"))
five_min = time.time() + 60*5
timeout = time.time() + 5
while True:
    cookie_img.click()
    if time.time() > timeout:
        costs = driver.find_elements(By.CSS_SELECTOR, "#store div b")
        prices_list = []
        for i in range(0, 8):
            prices_list.append(costs[i].text.split("-")[1].replace(",", ""))
        price_id_dict = {k:v for k,v in zip(prices_list,ids_list)}
        money = driver.find_element(By.ID, "money").text
        filered_dict = {int(k): v for k, v in price_id_dict.items() if int(k) <= int(money)}
        maximum_affordable_price = max(filered_dict.keys(), key=int)
        maximum_affordable_price_id = filered_dict.get(maximum_affordable_price, "Not found")
        driver.find_element(By.ID, f"{maximum_affordable_price_id}").click()
        timeout = time.time() + 5

        if time.time() > five_min:
            cookie_per_s = driver.find_element(By.ID, "cps").text
            print(cookie_per_s)
            break