import os
from dotenv import load_dotenv
from fake_useragent import UserAgent

# ✅ Correct way to use undetected-chromedriver via selenium-wire
from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions

load_dotenv()


def launch_browser(headless=True):
    key = os.getenv("SCRAPERAPI_KEY")
    if not key:
        raise EnvironmentError("SCRAPERAPI_KEY is missing in .env file")

    # 🔐 ScraperAPI authenticated proxy
    proxy_url = f"http://scraperapi:{key}@proxy-server.scraperapi.com:8001"

    # ✅ Selenium-Wire proxy config
    sw_options = {
        "proxy": {
            "http":  proxy_url,
            "https": proxy_url,
            "no_proxy": "localhost,127.0.0.1"
        }
    }

    # 🧠 Stealth browser flags
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")

    # 🧪 TEMP ONLY: Ignore SSL certs (so httpbin/github don't block you)
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--allow-running-insecure-content")

    # ❌ DO NOT add proxy-server manually — Selenium-Wire handles it

    driver = Chrome(options=options, seleniumwire_options=sw_options)
    return driver
