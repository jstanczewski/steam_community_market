import requests
import json
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
from decouple import config

cookie = {"steamLoginSecure": config("STEAM_LOGIN_SECURE")}
game_id = config("GAME_ID_1")


# with open("730_custom_item_names.docx", "rb") as file:
#     all_items_names = pickle.load(file)
all_items_names = [
    "UMP-45 | Crime Scene (Factory New)",
    "FAMAS | Prime Conspiracy (Factory New)",
    "FAMAS | Neural Net (Minimal Wear)",
    "Tec-9 | Bamboo Forest (Factory New)",
]
current_run = 1

for item in all_items_names:
    print(f"{str(current_run)} out of {str(len(all_items_names))}")
    print(f"DATA FOR: {item.upper()}")
    item_http = item.replace(" ", "%20")
    item_http = item_http.replace("&", "%26")
    item = requests.get(
        "https://steamcommunity.com/market/pricehistory/?appid="
        + game_id
        + "&market_hash_name="
        + item_http,
        cookies=cookie,
    )
    # print(f'{str(current_run)} out of {str(len(all_items_names))}, code:{str(item.status_code)}')
    current_run += 1
    item = item.content
    item = json.loads(item)
    if item:
        item_price_data = item["prices"]
        if not item_price_data:
            continue
        else:
            item_prices = []
            item_quantity = []
            item_date = []
            for current_day in item_price_data:
                item_prices.append(current_day[1])
                item_quantity.append(current_day[2])
                item_date.append(datetime.strptime(current_day[0][0:11], "%b %d %Y"))

            item_prices = list(map(float, item_prices))
            item_quantity = list(map(int, item_quantity))

            for current_day in range(len(item_date) - 1, 1, -1):
                if item_date[current_day] == item_date[current_day - 1]:
                    item_prices[current_day] = np.mean(
                        [item_prices[current_day], item_prices[current_day - 1]]
                    )
                    item_quantity[current_day] = np.sum(
                        [item_quantity[current_day], item_quantity[current_day - 1]]
                    )
                    del item_date[current_day]
                    del item_prices[current_day]
                    del item_quantity[current_day]

            norm_time = list(range(0, len(item_prices)))

            avg_price_today = round(item_prices[-1], 3)
            days_on_market = (datetime.today() - item_date[0]).days
            price_change_from_day_1 = round(item_prices[-1] - item_prices[0], 3)
            highest_price = max(item_prices)
            lowest_price = min(item_prices)
            highest_index = item_prices.index(highest_price)
            lowest_index = item_prices.index(lowest_price)
            diff_between_lowest_and_highest = round(highest_price - lowest_price, 3)
            avg_price = round(np.mean(item_prices), 3)
            avg_quantity = round(np.mean(item_quantity), 2)
            quantity_today = item_quantity[-1]

            price_change_past_5_days = 0
            price_change_past_10_days = 0
            price_change_past_30_days = 0
            percentage_price_change_past_5_days = 0
            percentage_price_change_past_10_days = 0
            percentage_price_change_past_30_days = 0

            if item_prices[-5]:
                price_change_past_5_days = round(item_prices[-1] - item_prices[-5], 3)
                percentage_price_change_past_5_days = round(
                    price_change_past_5_days / item_prices[-5] * 100, 2
                )
            if item_prices[-10]:
                price_change_past_10_days = round(item_prices[-1] - item_prices[-10], 3)
                percentage_price_change_past_10_days = round(
                    price_change_past_10_days / item_prices[-10] * 100, 2
                )
            if item_prices[-30]:
                price_change_past_30_days = round(item_prices[-1] - item_prices[-30], 3)
                percentage_price_change_past_30_days = round(
                    price_change_past_30_days / item_prices[-30] * 100, 2
                )
        print(f"Average price today: {avg_price_today} zł")
        print(f"Days on the market: {days_on_market}")
        print(
            f"Price change from the 1st day on the market: {price_change_from_day_1} zł"
        )
        print(f"Highest price ever: {highest_price} zł")
        print(f"Lowest price ever: {lowest_price} zł")
        print(f"Highest difference in price: {diff_between_lowest_and_highest} zł")
        print(f"Average price all time: {avg_price} zł")
        # print(f'Average quantity sold daily: {avg_quantity}')
        # print(f'Quantity sold today: {quantity_today}')
        print(f"Price change in the past 5 days: {price_change_past_5_days} zł")
        print(
            f"Percentage price change in the past 5 days: {percentage_price_change_past_5_days}%"
        )
        print(f"Price change in the past 10 days: {price_change_past_10_days} zł")
        print(
            f"Percentage price change in the past 10 days: {percentage_price_change_past_10_days}%"
        )
        print(f"Price change in the past 30 days: {price_change_past_30_days} zł")
        print(
            f"Percentage price change in the past 30 days: {percentage_price_change_past_30_days}%"
        )
        print("<--- --->")
        print("<--- --->")
        print("<--- --->")
