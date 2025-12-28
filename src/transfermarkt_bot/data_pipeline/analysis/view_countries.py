import json
import os

import geopandas as gpd
import matplotlib.pyplot as plt
from loguru import logger

DATA_DIR = "data/competitions"


def load_countries_data(folder_path: str) -> list[str]:
    # load JSON data in the folder
    countries = set()
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), "r") as f:
                data = json.load(f)
                for competition in data:
                    countries.add(competition["country_name"])
    return list(countries)


countries = load_countries_data(DATA_DIR)
name_mapping = {
    "Turkiye": "Turkey",
    "Czech Republic": "Czechia",
    "Bosnia-Herzegovina": "Bosnia and Herzegovina",
    "United States": "United States of America",
    "Chinese Taipei": "Taiwan",
    "Republic of Ireland": "Ireland",
    "Bosnia and Herzegovina": "Bosnia and Herz.",
    "Dominican Republic": "Dominican Rep.",
    "Faroe Islands": "Faeroe Is.",
    "England": "United Kingdom",
}
mapped_countries = [name_mapping.get(c, c) for c in countries]

# Load world map
# Natural Earth low resolution world map
url = "https://naturalearth.s3.amazonaws.com/50m_cultural/ne_50m_admin_0_countries.zip"


world = gpd.read_file(url)
missing_countries = set(mapped_countries) - set(world["NAME"])
if missing_countries:
    logger.warning(f"Missing countries in the world map: {missing_countries}")
# Create a flag column
world["highlight"] = world["NAME"].isin(mapped_countries)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))
world.plot(ax=ax, color="lightgrey", edgecolor="white")
world[world["highlight"]].plot(ax=ax, color="red")

ax.set_title("Extracted Countries")
ax.axis("off")
plt.show()
