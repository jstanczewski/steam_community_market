from collections import defaultdict
import numpy as np
from datetime import datetime
import SteamMarket
from time import sleep
from dotenv import dotenv_values

# COOKIE = {"steamLoginSecure": environ["STEAM_LOGIN_SECURE"]}
GAME_ID = dotenv_values('.env')['GAME_ID_1']
SteamMarket.set_cookies(dotenv_values('.env')["STEAM_LOGIN_SECURE"])
SteamMarket.iniate_cookies()

all_items_names = [
    "Sticker | FaZe Clan | Berlin 2019",
    "Sticker | CR4ZY | Berlin 2019",
    "Sticker | mousesports (Holo) | Berlin 2019",
    "Sticker | FaZe Clan (Holo) | Berlin 2019",
    "Sticker | Natus Vincere (Holo) | Berlin 2019",
    "Sticker | compLexity Gaming | Berlin 2019",
    "Sticker | mousesports (Foil) | Berlin 2019",
    "Sticker | Team Liquid (Holo) | Berlin 2019",
    "Sticker | Natus Vincere | Berlin 2019",
    "Sticker | Team Liquid | Berlin 2019",
    "Sticker | FaZe Clan (Foil) | Berlin 2019",
    "Lt. Commander Ricksaw | NSWC SEAL",
    "Sticker | ropz (Foil) | London 2018",
    "Operation Phoenix Weapon Case",
    "Shattered Web Case",
    "Galil AR | Akoben (Field-Tested)",
    "SSG 08 | Bloodshot (Field-Tested)",
    "SG 553 | Colony IV (Field-Tested)",
    "AK-47 | Rat Rod (Minimal Wear)",
    "AK-47 | Safari Mesh (Field-Tested)",
    "CZ75-Auto | Emerald Quartz (Factory New)",
    "MP9 | Stained Glass (Field-Tested)",
    "MAC-10 | Copper Borre (Minimal Wear)",
    "MAC-10 | Copper Borre (Factory New)",
    "M4A1-S | Moss Quartz (Factory New)",
]


def item_prices(item):
    item_prices = defaultdict(list)
    print(f"DATA FOR: {item.upper()}")
    item_name = item
    item = SteamMarket.get_price_history(GAME_ID, item)
    if item:
        item_price_data = item["prices"]
        date = []
        prices = []
        quantity = []
        for day in item_price_data:
            date.append(datetime.strptime(day[0][0:11], "%b %d %Y"))
            prices.append(day[1])
            quantity.append(day[2])
        for day in range(len(item_price_data) - 1, 1, -1):
            index = 1
            if prices[day] in item_prices[f"{date[day]}"]:
                continue
            else:
                for i in range(int(quantity[day])):
                    item_prices[f"{date[day]}"].append(prices[day])
            if date[day] == date[day - index]:
                for i in range(int(quantity[day - index])):
                    item_prices[f"{date[day]}"].append(prices[day - index])
                index += 1
            else:
                continue

    avg_price_today = round(np.mean(item_prices[list(item_prices.keys())[0]]), 2)
    avg_price_yesterday = round(np.mean(item_prices[list(item_prices.keys())[1]]), 2)
    avg_price_5_days_ago = round(np.mean(item_prices[list(item_prices.keys())[5]]), 2)
    avg_price_10_days_ago = round(np.mean(item_prices[list(item_prices.keys())[10]]), 2)
    avg_price_30_days_ago = round(np.mean(item_prices[list(item_prices.keys())[30]]), 2)
    percentage_price_change_yesterday = round(
        (avg_price_today - avg_price_yesterday) / avg_price_yesterday * 100, 2
    )
    percentage_price_change_5_days = round(
        (avg_price_today - avg_price_5_days_ago) / avg_price_5_days_ago * 100, 2
    )
    percentage_price_change_10_days = round(
        (avg_price_today - avg_price_10_days_ago) / avg_price_10_days_ago * 100, 2
    )
    percentage_price_change_30_days = round(
        (avg_price_today - avg_price_30_days_ago) / avg_price_30_days_ago * 100, 2
    )

    print(f"Average price today: {avg_price_today} zł")
    print(f"Average price yesterday: {avg_price_yesterday} zł")
    print(f"Percentage price change: {percentage_price_change_yesterday}%")
    print(f"Average price 5 days ago: {avg_price_5_days_ago} zł")
    print(f"Percentage price change: {percentage_price_change_5_days}%")
    print(f"Average price 10 days ago: {avg_price_10_days_ago} zł")
    print(f"Percentage price change: {percentage_price_change_10_days}%")
    print(f"Average price 30 days ago: {avg_price_30_days_ago} zł")
    print(f"Percentage price change: {percentage_price_change_30_days}%")
    return f"{item_name.upper()} \n\nAverage price today: {avg_price_today} zł \n\nAverage price yesterday: {avg_price_yesterday} zł \nPercentage price change: {percentage_price_change_yesterday}% \n\nAverage price 5 days ago: {avg_price_5_days_ago} zł \nPercentage price change: {percentage_price_change_5_days}% \n\nAverage price 10 days ago: {avg_price_10_days_ago} zł \nPercentage price change: {percentage_price_change_10_days}% \n\nAverage price 30 days ago: {avg_price_30_days_ago} zł \nPercentage price change: {percentage_price_change_30_days}% \n"


def item_quantity(item):
    item_quantities = defaultdict(list)
    item = SteamMarket.get_price_history(GAME_ID, item)
    if item:
        item_price_data = item["prices"]
        date = []
        quantity = []
        for day in item_price_data:
            date.append(datetime.strptime(day[0][0:11], "%b %d %Y"))
            quantity.append(day[2])
        for day in range(len(item_price_data) - 1, 1, -1):
            item_quantities[f"{date[day]}"].append(quantity[day])
    item_quantities[list(item_quantities.keys())[0]] = list(
        map(int, item_quantities[list(item_quantities.keys())[0]])
    )
    item_quantities[list(item_quantities.keys())[1]] = list(
        map(int, item_quantities[list(item_quantities.keys())[1]])
    )
    item_quantities[list(item_quantities.keys())[5]] = list(
        map(int, item_quantities[list(item_quantities.keys())[5]])
    )
    item_quantities[list(item_quantities.keys())[10]] = list(
        map(int, item_quantities[list(item_quantities.keys())[10]])
    )
    item_quantities[list(item_quantities.keys())[30]] = list(
        map(int, item_quantities[list(item_quantities.keys())[30]])
    )
    quantity_today = np.sum(item_quantities[list(item_quantities.keys())[0]])
    quantity_yesterday = np.sum(item_quantities[list(item_quantities.keys())[1]])
    quantity_5_days_ago = np.sum(item_quantities[list(item_quantities.keys())[5]])
    quantity_10_days_ago = np.sum(item_quantities[list(item_quantities.keys())[10]])
    quantity_30_days_ago = np.sum(item_quantities[list(item_quantities.keys())[30]])

    print(f"Quantity sold today: {quantity_today}")
    print(f"Quantity sold yesterday: {quantity_yesterday}")
    print(f"Quantity sold 5 days ago: {quantity_5_days_ago}")
    print(f"Quantity sold 10 days ago: {quantity_10_days_ago}")
    print(f"Quantity sold 30 days ago: {quantity_30_days_ago}")
    print("<--- --->")
    return f"Quantity sold today: {quantity_today} \nQuantity sold yesterday: {quantity_yesterday} \nQuantity sold 5 days ago: {quantity_5_days_ago} \nQuantity sold 10 days ago: {quantity_10_days_ago} \nQuantity sold 30 days ago: {quantity_30_days_ago}"


if __name__ == "__main__":
    current_run = 1
    for i in all_items_names:
        print(f"{str(current_run)} out of {str(len(all_items_names))}")
        item_prices(i)
        item_quantity(i)
        current_run += 1
        sleep(1)
