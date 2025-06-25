import csv
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# --- CONFIG ---
URL = "https://www.realtor.com/realestateandhomes-search/Brooklyn_NY"
PROXY = "YOUR_WEBSHARE_PROXY"  # e.g. username:password@ip:port

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def create_driver():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(f"--proxy-server=http://{PROXY}")
    for k, v in HEADERS.items():
        chrome_options.add_argument(f"--{k}={v}")

    driver = uc.Chrome(options=chrome_options)
    return driver


def scrape_realtor():
    driver = create_driver()
    driver.get(URL)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-testid='card-content']"))
        )
        time.sleep(2)

        listings = driver.find_elements(
            By.CSS_SELECTOR, "div[data-testid='card-content']")
        results = []

        for listing in listings:
            try:
                address1 = listing.find_element(
                    By.CSS_SELECTOR, "[data-testid='card-address-1']").text
                address2 = listing.find_element(
                    By.CSS_SELECTOR, "[data-testid='card-address-2']").text
                price = listing.find_element(
                    By.CSS_SELECTOR, "[data-testid='card-price']").text
                beds = listing.find_element(
                    By.CSS_SELECTOR, "[data-testid='property-meta-beds'] span").text
                baths = listing.find_element(
                    By.CSS_SELECTOR, "[data-testid='property-meta-baths'] span").text

                results.append({
                    "address": f"{address1}, {address2}",
                    "price": price,
                    "bedrooms": beds,
                    "bathrooms": baths
                })
            except Exception as e:
                print("Error parsing a listing:", e)

    finally:
        driver.quit()

    with open("realtor_listings.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["address", "price", "bedrooms", "bathrooms"])
        writer.writeheader()
        writer.writerows(results)
        print("✅ Exported to realtor_listings.csv")


if __name__ == "__main__":
    scrape_realtor()
