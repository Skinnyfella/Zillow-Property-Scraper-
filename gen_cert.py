import os
from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions
from fake_useragent import UserAgent

# ✅ Tell selenium-wire where to store the cert
os.environ['SELENIUM_WIRE_HOME'] = r"C:\Users\USER\Desktop\python\.seleniumwire"

# Set up undetected Chrome
options = ChromeOptions()
options.add_argument(f"user-agent={UserAgent().random}")
options.add_argument("--disable-blink-features=AutomationControlled")

print("🌱 Launching browser to trigger cert creation...")

driver = Chrome(options=options, seleniumwire_options={})
driver.get("https://example.com")

input("✅ Press Enter to close...")  # Wait a few secs before quitting
driver.quit()

# Check for certificate
cert_path = os.path.join(os.environ['SELENIUM_WIRE_HOME'], 'ca.crt')
if os.path.exists(cert_path):
    print(f"✅ Certificate found at: {cert_path}")
else:
    print(f"❌ Certificate NOT found at: {cert_path}\nTry visiting an HTTPS site and ensure Selenium Wire is intercepting traffic.")
