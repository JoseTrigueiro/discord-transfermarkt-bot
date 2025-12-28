from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://www.transfermarkt.com"

COUNTRY_URL = "/wettbewerbe/national/wettbewerbe/{country_id}"


def scrape_competitions_by_country(country_id: int) -> list[dict]:
    url = BASE_URL + COUNTRY_URL.format(country_id=country_id)
    headers = {"User-Agent": "Mozilla/5.0"}

    with httpx.Client(headers=headers) as client:
        res = client.get(url)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        # 1. Find the "Domestic leagues & cups" box
        box = soup.find("h2", string=lambda x: x and "Domestic leagues" in x)
        if not box:
            return []

        # The table is in the next sibling <div class="responsive-table">
        table = box.find_parent("div", class_="box").select_one("table.items")
        if not table:
            return []

        competitions = []
        current_type = None

        for row in table.select("tbody > tr"):
            # Detect section headers (First Tier, Second Tier, etc.)
            header = row.select_one("td.extrarow")
            if header:
                current_type = header.get_text(strip=True)
                continue

            # Detect competition rows
            cell = row.select_one("td.hauptlink table.inline-table")
            if not cell:
                continue

            links = cell.select("a")
            if len(links) < 2:
                continue

            a = links[1]  # second <a> is the competition name

            # Country name (from page header)
            country = (
                soup.select_one(".langer-text:contains('National teams')")
                .find_next("a")
                .get_text(strip=True)
            )

            competitions.append(
                {
                    "country_id": country_id,
                    "country_name": country,
                    "type": current_type,
                    "name": a.get_text(strip=True),
                    "url": urljoin(BASE_URL, a["href"]),
                }
            )

        return competitions


if __name__ == "__main__":
    comps = scrape_competitions_by_country(133)
    for comp in comps:
        print(comp)
