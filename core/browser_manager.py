import os
from seleniumwire import webdriver
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from dotenv import load_dotenv

load_dotenv()


def launch_browser(headless=True):
    key = os.getenv("SCRAPERAPI_KEY")
    proxy_url = f"http://scraperapi:{key}@proxy-server.scraperapi.com:8001"

    sw_options = {
        "proxy": {
            "http":  proxy_url,
            "https": proxy_url,
            "no_proxy": "localhost,127.0.0.1"
        }
    }

    options = uc.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument(
        "--proxy-server=http://proxy-server.scraperapi.com:8001")

    driver = uc.Chrome(options=options, seleniumwire_options=sw_options)
    return driver
