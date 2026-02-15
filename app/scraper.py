# app/scraper.py
import requests
from bs4 import BeautifulSoup

def get_leads():
    leads = []

    # Example URL - you can change to your target directory
    url = "https://www.yellowpages.com/search?search_terms=software&geo_location_terms=USA"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch leads")
        return leads

    soup = BeautifulSoup(response.text, "html.parser")
    businesses = soup.find_all("div", class_="result")

    for b in businesses:
        name_tag = b.find("a", class_="business-name")
        website_tag = b.find("a", class_="track-visit-website")
        email_tag = b.find("a", href=lambda x: x and "mailto:" in x)

        name = name_tag.text.strip() if name_tag else None
        website = website_tag.get("href") if website_tag else None
        email = email_tag.get("href").replace("mailto:", "") if email_tag else None

        if name and website:
            leads.append({
                "name": name,
                "website": website,
                "email": email or ""
            })

    return leads
