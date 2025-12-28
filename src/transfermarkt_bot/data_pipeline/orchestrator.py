import json
import os
import random
import time
from typing import Any, Callable

from loguru import logger

from transfermarkt_bot.data_pipeline.loaders.clubs import load_club_data
from transfermarkt_bot.data_pipeline.loaders.competitions import (
    load_competition_data,
)
from transfermarkt_bot.data_pipeline.scrapers.clubs import (
    scrape_clubs_by_competition,
)
from transfermarkt_bot.data_pipeline.scrapers.competitions import (
    scrape_competitions_by_country,
)
from transfermarkt_bot.data_pipeline.scrapers.players import (
    scrape_players_by_club,
)


class ScrapeOrchestrator:
    def __init__(
        self,
        base_folder: str = "data",
        competition_folder: str = "competitions",
        club_folder: str = "clubs",
        player_folder: str = "players",
    ):
        self.base_folder = base_folder
        self.competition_folder = base_folder + "/" + competition_folder
        self.club_folder = base_folder + "/" + club_folder
        self.player_folder = base_folder + "/" + player_folder
        self.min_wait_time = 1  # seconds
        self.max_wait_time = 3  # seconds
        self.competition_name_filter = "Tier"

    def run(
        self,
        scrape_competitions: bool = False,
        scrape_clubs: bool = False,
        scrape_players: bool = False,
    ):
        if scrape_competitions:
            self.run_competitions()
        df_comps = load_competition_data(self.competition_folder)

        competition_urls = df_comps["competition_url"].tolist()

        if scrape_clubs:
            self.run_clubs(competition_urls)
        df_clubs = load_club_data(self.club_folder)
        club_urls = df_clubs["club_url"].tolist()
        if scrape_players:
            self.run_players(club_urls)

    def _scrape_and_save(
        self,
        folder: str,
        items: list[Any],
        scrape_func: Callable[[Any], Any],
        get_id_func: Callable[[Any], str],
        log_message: str,
    ):
        """Generic method to scrape data and save to JSON files."""
        os.makedirs(folder, exist_ok=True)
        for item in items:
            logger.info(f"{log_message}: {item}")
            try:
                data = scrape_func(item)
            except Exception as e:
                logger.error(f"Failed to scrape {item}: {e}")
                continue

            file_id = get_id_func(item)
            with open(f"{folder}/{file_id}.json", "w") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            # Random wait time between requests
            wait_time = random.uniform(self.min_wait_time, self.max_wait_time)
            time.sleep(wait_time)

    def run_competitions(self):
        country_ids = list(range(0, 300))  # Wide sweep of country IDs
        self._scrape_and_save(
            folder=self.competition_folder,
            items=country_ids,
            scrape_func=scrape_competitions_by_country,
            get_id_func=lambda country_id: str(country_id),
            log_message="Scraping competitions for country ID",
        )

    def run_clubs(self, competition_urls: list[str]):
        self._scrape_and_save(
            folder=self.club_folder,
            items=competition_urls,
            scrape_func=scrape_clubs_by_competition,
            get_id_func=lambda url: url.split("/")[-1],
            log_message="Scraping clubs for competition URL",
        )

    def run_players(self, club_urls: list[str]):
        self._scrape_and_save(
            folder=self.player_folder,
            items=club_urls,
            scrape_func=scrape_players_by_club,
            get_id_func=lambda url: url.split("/")[-3],
            log_message="Scraping players for club URL",
        )


if __name__ == "__main__":
    orchestrator = ScrapeOrchestrator()
    orchestrator.run(scrape_clubs=False, scrape_competitions=False, scrape_players=True)
