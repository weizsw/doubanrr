import os

from dotenv import load_dotenv

import common
import consts
import db

load_dotenv()
SCHEDULE = int(os.getenv("SCHEDULE", "30"))
CLIENT_ID = common.get_env_variable("CLIENT_ID")
CLIENT_SECRET = common.get_env_variable("CLIENT_SECRET")
USER_NAME = common.get_env_variable("USER_NAME")
DOUBAN_RSS = common.get_env_variable("DOUBAN_RSS")
LIST_ID = common.get_env_variable("LIST_ID")
ACCESS_TOKEN, _ = db.get_token(consts.ACCESS_TOKEN_TYPE)
REFRESH_TOKEN, _ = db.get_token(consts.REFRESH_TOKEN_TYPE)

if not ACCESS_TOKEN or not REFRESH_TOKEN:
    ACCESS_TOKEN = common.get_env_variable("ACCESS_TOKEN")
    REFRESH_TOKEN = common.get_env_variable("REFRESH_TOKEN")
    db.set_token(ACCESS_TOKEN, consts.ACCESS_TOKEN_TYPE)
    db.set_token(REFRESH_TOKEN, consts.REFRESH_TOKEN_TYPE)
