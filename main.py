import time
from datetime import datetime, timedelta

from loguru import logger

import common
import consts
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
        trakt.add_season_to_list,
        trakt.add_episode_to_list,
    ]

    remove_functions = [
        trakt.remove_movie_from_list,
        trakt.remove_show_from_list,
        trakt.remove_season_from_list,
        trakt.remove_episode_from_list,
    ]

    token, added_time = db.get_token(consts.ACCESS_TOKEN_TYPE)
    if token:
        added_time = datetime.strptime(added_time, "%Y-%m-%d %H:%M:%S")
        if datetime.now() - added_time > timedelta(days=60):
            access_token, refresh_token = trakt.refresh_token()
            global_vars.ACCESS_TOKEN = access_token
            global_vars.REFRESH_TOKEN = refresh_token
            db.update_token(access_token, consts.ACCESS_TOKEN_TYPE)
            db.update_token(refresh_token, consts.REFRESH_TOKEN_TYPE)

    watched_movies = trakt.get_watched_movies()
    watched_shows = trakt.get_watched_shows()
    for movie in watched_movies:
        if not db.get_imdb_record(movie["movie"]["ids"]["imdb"]):
            db.set_imdb_record(
                movie["movie"]["ids"]["imdb"], watched=True, removed=False
            )
    for show in watched_shows:
        if not db.get_imdb_record(show["show"]["ids"]["imdb"]):
            db.set_imdb_record(show["show"]["ids"]["imdb"], watched=True, removed=False)

    for entry in feed:
        if not common.is_wanna_watch(entry.title):
            continue

        imdb_id = rss.get_imdb_id(entry.link)
        db_record = db.get_imdb_record(imdb_id)
        if db_record:
            _, watched, removed = db_record
            if removed:
                logger.info(f"{entry.title} with IMDb ID {imdb_id} has been removed.")
                continue
            if watched:
                for f in remove_functions:
                    if f(imdb_id):
                        db.set_imdb_record(imdb_id, watched=True, removed=True)
                        logger.info(
                            f"{entry.title} with IMDb ID {imdb_id} has been removed from the list."
                        )
                        break
                    time.sleep(1.1)
                logger.info(f"{entry.title} with IMDb ID {imdb_id} is already watched.")
                continue
            else:
                logger.info(f"{entry.title} with IMDb ID {imdb_id} already added.")
                continue

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
            logger.info(f"Waiting for {global_vars.SCHEDULE} minutes before next run.")
            time.sleep(global_vars.SCHEDULE * 60)
    else:
        main()
