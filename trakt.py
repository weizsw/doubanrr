import json

import requests
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed

import consts
import db
import global_vars


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def refresh_token():
    url = "https://api.trakt.tv/oauth/token"

    payload = json.dumps(
        {
            "refresh_token": global_vars.REFRESH_TOKEN,
            "client_id": global_vars.CLIENT_ID,
            "client_secret": global_vars.CLIENT_SECRET,
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
            "grant_type": "refresh_token",
        }
    )

    headers = {
        "trakt-api-version": "2",
        "Content-Type": "application/json",
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        logger.error(f"Encountered an error: {e}. Retrying in 3 seconds...")

    logger.info(response)
    if response.status_code != 200:
        logger.error(f"HTTP status code is {response.status_code}")

    response_json = response.json()
    access_token = response_json["access_token"]
    refresh_token = response_json["refresh_token"]
    db.set_token(access_token, consts.ACCESS_TOKEN_TYPE)
    db.set_token(refresh_token, consts.REFRESH_TOKEN_TYPE)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def add_movie_to_list(imdb_id):
    url = f"https://api.trakt.tv/users/{global_vars.USER_NAME}/lists/{global_vars.LIST_ID}/items"

    payload = json.dumps({"movies": [{"ids": {"imdb": imdb_id}}]})
    headers = {
        "trakt-api-version": "2",
        "trakt-api-key": global_vars.CLIENT_ID,
        "Authorization": "Bearer " + global_vars.ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        logger.error(f"Encountered an error: {e}. Retrying in 3 seconds...")

    if response.status_code != 201:
        logger.error(f"HTTP status code is {response.status_code}")

    response_json = response.json()
    if (
        response_json["added"]["movies"] == 0
        and not response_json["not_found"]["movies"]
    ):
        logger.debug(f"IMDb ID {imdb_id} already added.")
    if response_json["not_found"]["movies"]:
        logger.debug(f"IMDb ID {imdb_id} not found in movies.")
    return True if response_json["added"]["movies"] == 1 else False


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def add_show_to_list(imdb_id):
    url = f"https://api.trakt.tv/users/{global_vars.USER_NAME}/lists/{global_vars.LIST_ID}/items"

    payload = json.dumps({"shows": [{"ids": {"imdb": imdb_id}}]})
    headers = {
        "trakt-api-version": "2",
        "trakt-api-key": global_vars.CLIENT_ID,
        "Authorization": "Bearer " + global_vars.ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        logger.error(f"Encountered an error: {e}. Retrying in 3 seconds...")

    if response.status_code != 201:
        logger.error(f"HTTP status code is {response.status_code}")

    response_json = response.json()
    if response_json["added"]["shows"] == 0 and not response_json["not_found"]["shows"]:
        logger.debug(f"IMDb ID {imdb_id} already added.")
    if response_json["not_found"]["shows"]:
        logger.debug(f"IMDb ID {imdb_id} not found in shows.")
    return True if response_json["added"]["shows"] == 1 else False


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def add_season_to_list(imdb_id):
    url = f"https://api.trakt.tv/users/{global_vars.USER_NAME}/lists/{global_vars.LIST_ID}/items"

    payload = json.dumps({"seasons": [{"ids": {"imdb": imdb_id}}]})
    headers = {
        "trakt-api-version": "2",
        "trakt-api-key": global_vars.CLIENT_ID,
        "Authorization": "Bearer " + global_vars.ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        logger.error(f"Encountered an error: {e}. Retrying in 3 seconds...")

    if response.status_code != 201:
        logger.error(f"HTTP status code is {response.status_code}")

    response_json = response.json()
    if (
        response_json["added"]["seasons"] == 0
        and not response_json["not_found"]["seasons"]
    ):
        logger.debug(f"IMDb ID {imdb_id} already added.")
    if response_json["not_found"]["seasons"]:
        logger.debug(f"IMDb ID {imdb_id} not found in seasons.")
    return True if response_json["added"]["seasons"] == 1 else False


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def add_episode_to_list(imdb_id):
    url = f"https://api.trakt.tv/users/{global_vars.USER_NAME}/lists/{global_vars.LIST_ID}/items"

    payload = json.dumps({"episodes": [{"ids": {"imdb": imdb_id}}]})
    headers = {
        "trakt-api-version": "2",
        "trakt-api-key": global_vars.CLIENT_ID,
        "Authorization": "Bearer " + global_vars.ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        logger.error(f"Encountered an error: {e}. Retrying in 3 seconds...")

    if response.status_code != 201:
        logger.error(f"HTTP status code is {response.status_code}")

    response_json = response.json()
    if (
        response_json["added"]["episodes"] == 0
        and not response_json["not_found"]["episodes"]
    ):
        logger.debug(f"IMDb ID {imdb_id} already added.")
    if response_json["not_found"]["episodes"]:
        logger.debug(f"IMDb ID {imdb_id} not found in episodes.")
    return True if response_json["added"]["episodes"] == 1 else False
