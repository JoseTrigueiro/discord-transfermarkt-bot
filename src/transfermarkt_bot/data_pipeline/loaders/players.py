import json
import os

import pandas as pd


def load_player_url_data(folder: str) -> pd.DataFrame:
    player_data = []
    for filename in os.listdir(folder):
        if not filename.endswith(".json"):
            continue
        with open(os.path.join(folder, filename), "r") as f:
            competitions = json.load(f)
            for competition in competitions:
                # Extract league_id from URL (last part after last /)
                competition["player_id"] = competition["url"].rstrip("/").split("/")[-1]
            player_data.extend(competitions)
    player_df = pd.DataFrame(player_data)
    player_df = player_df.rename(columns={"name": "player_name", "url": "player_url"})
    return player_df


if __name__ == "__main__":
    df_players = load_player_url_data("data/players")
    print(len(df_players))
