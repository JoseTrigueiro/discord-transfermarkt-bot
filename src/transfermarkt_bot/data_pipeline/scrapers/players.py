import httpx
from bs4 import BeautifulSoup


def scrape_players_by_club(url: str) -> list[dict]:
    headers = {"User-Agent": "Mozilla/5.0"}

    with httpx.Client(headers=headers) as client:
        res = client.get(url)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        players = []

    for a in soup.select("table.items td.posrela table.inline-table td.hauptlink a"):
        name = a.get_text(strip=True)
        link = a["href"]
        full_link = f"https://www.transfermarkt.com{link}"

        players.append({"name": name, "url": full_link})

    return players


if __name__ == "__main__":
    players = scrape_players_by_club(
        "https://www.transfermarkt.com/fc-barcelona/kader/verein/131/saison_id/2023"
    )
    print(players)
