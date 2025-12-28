import json
import os

import pandas as pd


def load_competition_data(folder: str) -> pd.DataFrame:
    competition_data = []
    for filename in os.listdir(folder):
        if not filename.endswith(".json"):
            continue
        with open(os.path.join(folder, filename), "r") as f:
            competitions = json.load(f)
            for competition in competitions:
                # Extract league_id from URL (last part after last /)
                competition["league_id"] = competition["url"].rstrip("/").split("/")[-1]
            competition_data.extend(competitions)
    competition_df = pd.DataFrame(competition_data)
    competition_df = competition_df.rename(
        columns={"name": "competition_name", "url": "competition_url"}
    )
    return competition_df
