import requests
import json
import pickle
import pandas as pd
import numpy as np
import scipy.stats as sci
from datetime import datetime
import time
import random
from decouple import config

cookie = {'steamLoginSecure': config('STEAM_LOGIN_SECURE')}
game_id = config('GAME_ID_1')

all_items_names = []
all_items_get = requests.get("https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&appid="+game_id+"&norender=1&count=100", cookies=cookie)
all_items = all_items_get.content
all_items = json.loads(all_items)
total_items = all_items['total_count']
print(total_items)
