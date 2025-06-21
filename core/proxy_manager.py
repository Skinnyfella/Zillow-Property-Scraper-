import os
from dotenv import load_dotenv

load_dotenv()


def get_proxy():
    key = os.getenv("SCRAPERAPI_KEY")
    if not key:
        raise ValueError("SCRAPERAPI_KEY not found in .env")

    return f"http://scraperapi:{key}@proxy-server.scraperapi.com:8001"
