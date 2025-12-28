import httpx
from bs4 import BeautifulSoup


def scrape_clubs_by_competition(competition_url: str) -> list[dict]:
    headers = {"User-Agent": "Mozilla/5.0"}

    with httpx.Client(headers=headers) as client:
        res = client.get(competition_url)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
    # Find the table
    table = soup.find("table", class_="items")

    # Extract club names and links
    clubs = []
    for row in table.tbody.find_all("tr"):
        club_cell = row.find("td", class_="hauptlink no-border-links")
        if club_cell:
            a_tag = club_cell.find("a", href=True)
            name = a_tag.text.strip()
            link = BASE_URL + a_tag["href"]
            clubs.append({"name": name, "link": link})

    return clubs


if __name__ == "__main__":
    scrape_clubs_by_competition(
        "https://www.transfermarkt.pt/liga-portugal/startseite/wettbewerb/PO1"
    )
