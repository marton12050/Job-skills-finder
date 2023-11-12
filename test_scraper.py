import requests
from dotenv import load_dotenv
import os

load_dotenv()
SCRAPER_API = os.environ.get("SCRAPER_API")
SCRAPER_KEY = os.environ.get("SCRAPER_KEY")

url = f"https://{SCRAPER_API}/jobs"

payload = {
	"title": " ",
	"location": "Budapest",
	"rows": 300,
	"publishedAt": "Past24Hours"
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": SCRAPER_KEY,
	"X-RapidAPI-Host": SCRAPER_API
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
	print(response.json())
else:
	print("Error occurred during API call")
