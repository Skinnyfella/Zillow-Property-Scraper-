# Human behaviour simulation module
import time
import random
from selenium.webdriver.common.action_chains import ActionChains


def random_wait(a=1.0, b=3.0):
    time.sleep(random.uniform(a, b))


def simulate_scroll(driver):
    for _ in range(random.randint(1, 3)):
        scroll_by = random.randint(200, 800)
        driver.execute_script(f"window.scrollBy(0, {scroll_by});")
        random_wait(0.5, 2)


def simulate_mouse_move(driver):
    actions = ActionChains(driver)
    body = driver.find_element("tag name", "body")
    actions.move_to_element(body).perform()
    random_wait(0.5, 1.5)
