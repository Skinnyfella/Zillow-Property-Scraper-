import csv
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.browser_manager import launch_browser

# --- CONFIG ---
ZILLOW_URL = "https://www.zillow.com/homes/for_sale/Long-Island-City,-NY_rb/"


def scrape_zillow():
    driver = launch_browser(headless=False)
    driver.get(ZILLOW_URL)

    print("🧠 Solve CAPTCHA if needed...")
    input("✅ Press Enter after solving CAPTCHA manually...")

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "article[data-test='property-card']"))
        )

        listings = driver.find_elements(
            By.CSS_SELECTOR, "article[data-test='property-card']")
        results = []

        for listing in listings:
            try:
                address = listing.find_element(By.TAG_NAME, "address").text
                price = listing.find_element(
                    By.CSS_SELECTOR, "[data-test='property-card-price']").text
                detail_items = listing.find_elements(By.CSS_SELECTOR, "ul li")

                beds, baths = "", ""
                if len(detail_items) >= 2:
                    beds = detail_items[0].text
                    baths = detail_items[1].text

                link_elem = listing.find_element(
                    By.CSS_SELECTOR, "a.property-card-link")
                url = link_elem.get_attribute("href")

                results.append({
                    "address": address,
                    "price": price,
                    "bedrooms": beds,
                    "bathrooms": baths,
                    "url": url
                })
            except Exception as e:
                print("⚠️ Error extracting a listing:", e)

    finally:
        driver.quit()

    with open("zillow_listings.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["address", "price", "bedrooms", "bathrooms", "url"])
        writer.writeheader()
        writer.writerows(results)
        print("✅ Exported to zillow_listings.csv")


if __name__ == "__main__":
    scrape_zillow()
