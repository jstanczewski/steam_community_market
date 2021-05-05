import requests
import json
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from decouple import config

cookie = {'steamLoginSecure': config('STEAM_LOGIN_SECURE')}
game_id = config('GAME_ID_1')


with open(config('GAME_ID_1') + '_item_names.txt', 'rb') as file:
    all_items_names = pickle.load(file)
    all_items_names = all_items_names

all_items_pd = pd.DataFrame(data=None, index=None, columns=['item_name', 'current_price', 'initial', 'days_on_market', 'price_increase', 'price_avg', 'max_price', 'max_idx', 'min_price', 'min_idx', 'swing'])
current_run = 1

for current_item in all_items_names:
    current_item_http = current_item.replace(' ', '%20')
    current_item_http = current_item_http.replace('&', '%26')
    item = requests.get('https://steamcommunity.com/market/pricehistory/?appid='+game_id+'&market_hash_name='+current_item_http, cookies=cookie)
    print(f'{str(current_run)} out of {str(len(all_items_names))}, code: {str(item.status_code)}')
    current_run += 1
    item = item.content
    item = json.loads(item)
    if item:
        item_price_data = item['prices']
        if not item_price_data:
            continue
        else:
            item_prices = []
            item_date = []
            for current_day in item_price_data:
                item_prices.append(current_day[1])
                item_date.append(datetime.strptime(current_day[0][0:11], '%b %d %Y'))

            item_prices = list(map(float, item_prices))

            for current_day in range(len(item_date) - 1, 1, -1):
                if item_date[current_day] == item_date[current_day - 1]:
                    item_prices[current_day - 1] = np.mean([item_prices[current_day], item_prices[current_day - 1]])
                    del item_date[current_day]
                    del item_prices[current_day]

            norm_time = list(range(0, len(item_prices)))

            current_price = round(item_prices[-1], 3)
            days_on_market = (datetime.today() - item_date[0]).days
            price_increase = round(item_prices[-1] - item_prices[0], 3)
            max_price = max(item_prices)
            max_idx = item_prices.index(max_price)
            min_price = min(item_prices)
            min_idx = item_prices.index(min_price)
            swing = round(max_price - min_price, 3)
            item_price_avg = round(np.mean(item_prices), 3)
            if len(item_prices) > 1:
                item_price_initial = round(item_prices[1] - item_prices[0], 3)
            else:
                item_price_initial = round(item_prices[0], 3)

            current_item_dict = {'item_name': current_item, 'current_price': current_price, 'initial': item_price_initial, 'days_on_market': days_on_market, 'price_increase': price_increase, 'price_avg': item_price_avg, 'max_price': max_price, 'max_idx': max_idx, 'min_price': min_price, 'min_idx': min_idx, 'swing': swing}
            current_item_pd = pd.DataFrame(current_item_dict, index=[0])
            all_items_pd = all_items_pd.append(current_item_pd, ignore_index=True)

    else:
        continue

print('All the item data collected')
all_items_pd.to_csv(game_id + '_price_data.csv')
