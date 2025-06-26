import os
import time
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

COOKIES_FOLDER = "cookies"
os.makedirs(COOKIES_FOLDER, exist_ok=True)


def scroll_page(driver, depth=15):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(depth):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def save_cookies(driver, filename):
    filepath = os.path.join(COOKIES_FOLDER, filename)
    with open(filepath, "wb") as f:
        pickle.dump(driver.get_cookies(), f)


def load_cookies(driver, filename):
    filepath = os.path.join(COOKIES_FOLDER, filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                except Exception:
                    pass
