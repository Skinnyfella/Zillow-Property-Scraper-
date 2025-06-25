from undetected_chromedriver import Chrome, ChromeOptions
from fake_useragent import UserAgent


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

    driver = Chrome(
        options=options,
        version_main=137)

    return driver
