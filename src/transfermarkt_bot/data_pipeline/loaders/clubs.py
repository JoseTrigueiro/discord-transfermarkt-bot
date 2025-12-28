import json
import os

import pandas as pd


def load_club_data(folder: str) -> pd.DataFrame:
    club_data = []
    for filename in os.listdir(folder):
        if not filename.endswith(".json"):
            continue
        # Extract league_id from filename (e.g., "123.json" -> "123")
        league_id = os.path.splitext(filename)[0]
        with open(os.path.join(folder, filename), "r") as f:
            clubs = json.load(f)
            # Add league_id to each club record
            for club in clubs:
                club["league_id"] = league_id
                # Extract club_id from URL (part after /verein/)
                url_parts = club["link"].split("/")
                verein_index = url_parts.index("verein")
                club["club_id"] = int(url_parts[verein_index + 1])
            club_data.extend(clubs)
    club_df = pd.DataFrame(club_data)
    club_df = club_df.rename(columns={"name": "club_name", "link": "club_url"})
    return club_df
