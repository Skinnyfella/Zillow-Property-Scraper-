import os
from dotenv import load_dotenv
from fake_useragent import UserAgent
from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions

load_dotenv()

PROXY_ADDRESS = os.getenv("PROXY_ADDRESS")
PROXY_PORT = os.getenv("PROXY_PORT")
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")


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
        seleniumwire_options = {
            'proxy': {
                'http': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_ADDRESS}:{PROXY_PORT}',
                'https': f'https://{PROXY_USER}:{PROXY_PASS}@{PROXY_ADDRESS}:{PROXY_PORT}',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }

    driver = Chrome(
        options=options,
        seleniumwire_options=seleniumwire_options,
        version_main=137
    )

    return driver
