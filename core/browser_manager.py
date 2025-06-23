"""
core/browser_manager.py
————————————————————————————————————————
Launches an undetected-chromedriver instance routed
through ScraperAPI (via Selenium-Wire) and suppresses
SSL-certificate warnings so you don’t see the
‘Your connection is not private / ERR_CERT_AUTHORITY_INVALID’
screen while testing.

⚠️  Only use the “ignore-certificate-errors” flags in a
     dev or test environment.  Remove them for production
     once you have the CA cert trusted.
"""

import os
from dotenv import load_dotenv

# Stealth browser & proxy helpers
import undetected_chromedriver as uc
from seleniumwire import webdriver              # Selenium-Wire proxy layer
from fake_useragent import UserAgent            # Random UA strings

# ---------------------------------------------------------------------------

load_dotenv()                                   # pulls SCRAPERAPI_KEY from .env


def launch_browser(headless: bool = False):
    """
    Launch a stealth Chrome instance routed through ScraperAPI
    and ignoring SSL-certificate errors (testing only).

    Returns
    -------
    seleniumwire.webdriver.Chrome
    """
    # -----------------------------------------------------------------------
    # 1.  Build Selenium-Wire proxy settings
    # -----------------------------------------------------------------------
    api_key = os.getenv("SCRAPERAPI_KEY")
    if not api_key:
        raise EnvironmentError("SCRAPERAPI_KEY missing in your .env file")

    proxy_url = f"http://scraperapi:{api_key}@proxy-server.scraperapi.com:8001"

    sw_options = {
        "proxy": {
            "http":  proxy_url,
            "https": proxy_url,
            "no_proxy": "localhost,127.0.0.1"
        }
    }

    # -----------------------------------------------------------------------
    # 2.  Chrome options (stealth + SSL-ignore flags for dev)
    # -----------------------------------------------------------------------
    uc_options = uc.ChromeOptions()

    if headless:
        uc_options.add_argument("--headless=new")

    # Stealth flags
    uc_options.add_argument("--disable-blink-features=AutomationControlled")
    uc_options.add_argument(f"user-agent={UserAgent().random}")
    uc_options.add_argument("--no-sandbox")
    uc_options.add_argument("--disable-dev-shm-usage")
    uc_options.add_argument("--disable-extensions")
    uc_options.add_argument("--disable-infobars")

    # ❗ Testing-only flags – bypass privacy warning
    uc_options.add_argument("--ignore-certificate-errors")
    uc_options.add_argument("--allow-insecure-localhost")
    uc_options.add_argument("--allow-running-insecure-content")

    # NOTE: DO NOT add a separate --proxy-server flag here.
    # Selenium-Wire handles the proxy + authentication internally.

    # -----------------------------------------------------------------------
    # 3.  Launch undetected Chrome wrapped by Selenium-Wire
    # -----------------------------------------------------------------------
    driver = uc.Chrome(
        options=uc_options,
        seleniumwire_options=sw_options,
    )

    return driver
