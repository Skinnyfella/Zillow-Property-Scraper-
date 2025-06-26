import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.browser_manager import launch_browser
from core.utils import scroll_page, save_cookies, load_cookies

# --- CONFIG ---
BASE_URL = "https://www.zillow.com/homes/for_sale/Long-Island-City,-NY_rb/"
COOKIES_FILE = "zillow_cookies.pkl"
PAGES_TO_SCRAPE = 5


def generate_page_url(base_url, page_num):
    return f"{base_url}{page_num}_p/"


def extract_listings(driver):
    listings = driver.find_elements(
        By.CSS_SELECTOR, "article[data-test='property-card']"
    )
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

            url = listing.find_element(
                By.CSS_SELECTOR, "a.property-card-link").get_attribute("href")

            results.append({
                "address": address,
                "price": price,
                "bedrooms": beds,
                "bathrooms": baths,
                "url": url
            })
        except Exception as e:
            print("⚠️ Error extracting a listing:", e)

    return results


def scrape_zillow():
    driver = launch_browser(headless=False)

    # Load Zillow homepage
    driver.get("https://www.zillow.com/")
    load_cookies(driver, COOKIES_FILE)

    # Visit target base URL
    driver.get(BASE_URL)

    print("🧠 Solve CAPTCHA if needed...")
    input("✅ Press Enter after solving CAPTCHA manually...")

    save_cookies(driver, COOKIES_FILE)

    all_results = []

    for page in range(1, PAGES_TO_SCRAPE + 1):
        page_url = generate_page_url(BASE_URL, page)
        print(f"📄 Visiting page {page}: {page_url}")
        driver.get(page_url)

        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "article[data-test='property-card']")
                )
            )
        except Exception:
            print("⚠️ Timeout, retrying after 5s...")
            time.sleep(5)
            driver.refresh()
            WebDriverWait(driver, 40).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "article[data-test='property-card']")
                )
            )

        scroll_page(driver, depth=15)
        listings = extract_listings(driver)
        all_results.extend(listings)

    driver.quit()

    with open("zillow_listings.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["address", "price", "bedrooms", "bathrooms", "url"]
        )
        writer.writeheader()
        writer.writerows(all_results)

    print(
        f"✅ Scraped {len(all_results)} listings from {PAGES_TO_SCRAPE} pages.")
    print("📝 Saved to zillow_listings.csv")


if __name__ == "__main__":
    scrape_zillow()
