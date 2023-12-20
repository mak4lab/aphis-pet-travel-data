from bs4 import BeautifulSoup
from csv import DictWriter
from requests import get
from time import sleep
from urllib.parse import urljoin

base_url = "https://www.aphis.usda.gov/aphis/pet-travel/take-pet-to-foreign-country/export-pets"
response = get(base_url)
soup = BeautifulSoup(response.text)

options = soup.select("#country option")

print(options)

rows = []

for opt in options:
  name = opt.text
  attrs = opt.attrs
  url_path = opt.attrs['value']
  full_url = urljoin(base_url, url_path)

  if attrs['value'] == "#": continue

  row = {
    "name": name,
    "url": full_url
  }

  banner_color = "unknown"

  colors = ["Green", "Orange", "Purple", "Red", "Yellow"]
  for color in colors:
    if color.lower() in url_path.lower():
      banner_color = color.lower()
  
  if banner_color is "unknown":
    page_text = get(full_url).text
    for color in colors:
      if f'"{color} Banner" Country' in page_text:
        banner_color = color.lower()
  
  row['color'] = banner_color

  rows.append(row)

  print(row)

  sleep(1)

with open("./data/countries.csv", "w") as f:
  writer = DictWriter(f, fieldnames=["name", "color", "url"])
  writer.writeheader()
  for row in rows:
    writer.writerow(row)

