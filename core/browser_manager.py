import os
from dotenv import load_dotenv
from fake_useragent import UserAgent

from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions

load_dotenv()


def launch_browser(headless=True):
    # 🌐 Webshare Proxy Setup (Individual Proxy)
    proxy_host = os.getenv("WEBSHARE_HOST")
    proxy_port = os.getenv("WEBSHARE_PORT")
    proxy_user = os.getenv("WEBSHARE_USER")
    proxy_pass = os.getenv("WEBSHARE_PASS")

    if not all([proxy_host, proxy_port, proxy_user, proxy_pass]):
        raise EnvironmentError("❌ Missing Webshare proxy credentials in .env")

    proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"

    # ✅ Selenium-Wire proxy config
    sw_options = {
        "proxy": {
            "http": proxy_url,
            "https": proxy_url,
            "no_proxy": "localhost,127.0.0.1"
        }
    }

    # 🧠 Stealth Chrome setup
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")

    # 🧪 Dev SSL bypass (DO NOT keep in prod)
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--allow-running-insecure-content")

    driver = Chrome(
        options=options,
        seleniumwire_options=sw_options
    )

    # Properly override User-Agent
    driver.header_overrides = {
        'User-Agent': UserAgent().random
    }

    return driver
