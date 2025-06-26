import os
import pickle
from dotenv import load_dotenv
from fake_useragent import UserAgent
from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions

load_dotenv()

PROXY_ADDRESS = os.getenv("PROXY_ADDRESS")
PROXY_PORT = os.getenv("PROXY_PORT")
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")

COOKIES_FOLDER = "cookies"
os.makedirs(COOKIES_FOLDER, exist_ok=True)


def launch_browser(headless=True):
    options = ChromeOptions()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument(f"user-agent={UserAgent().random}")

    seleniumwire_options = {}

    if all([PROXY_ADDRESS, PROXY_PORT, PROXY_USER, PROXY_PASS]):
        proxy_str = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_ADDRESS}:{PROXY_PORT}"
        seleniumwire_options = {
            'proxy': {
                'http': proxy_str,
                'https': proxy_str,
                'no_proxy': 'localhost,127.0.0.1,github.com,raw.githubusercontent.com'
            }
        }
        print("✅ Proxy applied:", proxy_str)
    else:
        print("⚠️ Proxy not applied. Missing or invalid .env values.")

    driver = Chrome(
        options=options,
        seleniumwire_options=seleniumwire_options,
        version_main=137
    )

    return driver


def save_cookies(driver, filename):
    filepath = os.path.join(COOKIES_FOLDER, filename)
    with open(filepath, "wb") as file:
        pickle.dump(driver.get_cookies(), file)


def load_cookies(driver, filename):
    filepath = os.path.join(COOKIES_FOLDER, filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                try:
                    driver.add_cookie(cookie)
                except Exception:
                    pass
