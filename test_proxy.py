import requests
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("SCRAPERAPI_KEY")
proxy = f"http://scraperapi:{key}@proxy-server.scraperapi.com:8001"

proxies = {
    "http":  proxy,
    "https": proxy,
}

# ✅ Try a site ScraperAPI allows
url = "http://example.com"

print("🛰️ Sending request through ScraperAPI proxy...")
response = requests.get(url, proxies=proxies, timeout=20)
print("🧠 Response Status:", response.status_code)
