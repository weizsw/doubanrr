# Douban to Trakt Synchronizer

This Python application synchronizes movie and TV show information from Douban RSS feeds to a Trakt list. It's designed to automatically update your Trakt list with items you're interested in watching, based on the RSS feed from Douban.

## Features

- **RSS Feed Parsing**: Fetches and parses RSS feed from Douban for movies and TV shows.
- **Trakt Integration**: Adds movies, TV shows, seasons, and episodes to your Trakt list based on the RSS feed.
- **Token Refresh**: Automatically refreshes Trakt access tokens when they expire.
- **Duplicate Check**: Checks if an item is already added to the database before adding it to Trakt to avoid duplicates.
- **Logging**: Logs actions and errors for debugging and tracking.

## Requirements

- Python 3.x
- External libraries: `requests`, `datetime`, `logging`, and any other libraries required by `rss`, `trakt`, `db`, and `common` modules.
- A Douban RSS feed URL.
- Trakt API credentials: Client ID, Client Secret, and an initial Access Token.

## Setup

1. Clone this repository to your local machine.
2. Install the required Python libraries by running `pip install -r requirements.txt` (ensure you have `pip` installed).
3. Set up your Trakt API credentials and Douban RSS feed URL in a configuration file or environment variables (refer to the `trakt` and `rss` module documentation for details).
4. Ensure the `db` module is configured correctly to connect to your database.

## Usage

To run the synchronizer, execute the following command in your terminal:

```bash
python main.py
