import time

from loguru import logger

import common
import db
import global_vars
import rss
import trakt


def main():
    feed = rss.get_douban_rss()
    if feed is None:
        logger.error("Failed to get the RSS feed.")
        return

    add_functions = [
        trakt.add_movie_to_list,
        trakt.add_show_to_list,
        trakt.add_episode_to_list,
        trakt.add_season_to_list,
    ]
    for entry in feed:
        if not common.is_wanna_watch(entry.title):
            continue

        imdb_id = rss.get_imdb_id(entry.link)
        for f in add_functions:
            if f(imdb_id):
                db.set_imdb_record(imdb_id)
                logger.info(
                    f"{entry.title} with IMDb ID {imdb_id} has been added to the list."
                )
                break
            time.sleep(1.1)


if __name__ == "__main__":
    if global_vars.SCHEDULE > 0:
        while True:
            main()
            print(f"Waiting for {global_vars.SCHEDULE} minutes before next run.")
            time.sleep(global_vars.SCHEDULE * 60)
    else:
        main()
