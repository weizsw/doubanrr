import feedparser
import requests
from bs4 import BeautifulSoup
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_fixed

import global_vars


def get_douban_rss():
    url = global_vars.DOUBAN_RSS
    feed = feedparser.parse(url)
    return feed.entries


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_imdb_id(link):
    url = link
    payload = {}
    headers = {
        "Cookie": 'bid=CM-ebRtavcY; ll="108296"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except Exception as e:
        logger.error(f"Encountered an error: {e}. Retrying in 3 seconds...")
    if response.status_code != 200:
        logger.error(f"HTTP status code is {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    imdb_span = soup.find("span", string="IMDb:")
    imdb_id = imdb_span.next_sibling.strip()
    logger.info(f"Got IMDb ID: {imdb_id} from {url}")

    return imdb_id
