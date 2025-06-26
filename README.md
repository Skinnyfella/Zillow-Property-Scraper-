🕵️ Zillow Property Scraper (Stealth Web Scraping with Selenium)

This is a stealth web scraping framework built to extract real estate listings from [Zillow](https://www.zillow.com/) using **Selenium**, **undetected-chromedriver**, and optional **rotating proxy support** (e.g. Webshare or ScraperAPI). It simulates human behavior and handles login/captcha sessions with cookie persistence.

---

## 🚀 Features

- ✅ Headless Chrome (undetected)
- ✅ Stealth browser setup
- ✅ Auto-scroll and wait for dynamic content
- ✅ Cookie saving/loading to bypass CAPTCHA
- ✅ Proxy support via `.env` (Webshare/ScraperAPI)
- ✅ Structured CSV export
- ✅ Clean modular structure

---

## 📂 Project Structure

stealth_scraper/
├── core/
│ ├── browser_manager.py # Sets up Chrome with proxy and options
│ └── utils.py # Reusable functions (scroll, cookies)
├── search_scraper.py # Zillow scraper logic
├── .env # Proxy + config variables
├── zillow_listings.csv # Output CSV
└── README.md

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 1. Clone and install dependencies

```bash
git clone https://github.com/your-username/zillow-stealth-scraper.git
cd zillow-stealth-scraper
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
2. Create your .env file
env
Copy
Edit
USE_PROXY=True
PROXY_ADDRESS=proxy.webshare.io
PROXY_PORT=8000
PROXY_USER=your_username
PROXY_PASS=your_password
To disable proxy, set USE_PROXY=False.

3. Run the scraper
bash
Copy
Edit
python search_scraper.py
Solve CAPTCHA manually in the browser window (once).

Scraped listings will be saved to zillow_listings.csv.

📊 Output Sample
Address	Price	Bedrooms	Bathrooms	URL
12-45 45th Ave, NY	$899,000	2 bd	2 ba	https://www.zillow.com/...
21-10 42nd Rd #5B, NY	$749,500	1 bd	1 ba	https://www.zillow.com/...

🔐 Notes
This is for educational purposes only. Always respect robots.txt and site terms.

Zillow may rate-limit or block aggressive scraping — rotate IPs and handle gracefully.

```
