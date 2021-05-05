import requests
import json
import pickle
from decouple import config

cookie = {"steamLoginSecure": config("STEAM_LOGIN_SECURE")}
game_id = config("GAME_ID_1")

all_items_names = []
all_items_get = requests.get(
    "https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&appid="
    + game_id
    + "&norender=1&count=100",
    cookies=cookie,
)
all_items = all_items_get.content
all_items = json.loads(all_items)
total_items = all_items["total_count"]
print(total_items)

for current_position in range(0, total_items + 50, 50):
    all_items_get = requests.get(
        "https://steamcommunity.com/market/search/render/?start="
        + str(current_position)
        + "&count=100&search_descriptions=0&sort_column=default&sort_dir=desc&appid="
        + game_id
        + "&norender=1&count=5000",
        cookies=cookie,
    )
    print(
        f"Items {str(current_position)} out of {str(total_items)}, code: {str(all_items_get.status_code)}"
    )
    all_items = all_items_get.content
    all_items = json.loads(all_items)
    all_items = all_items["results"]
    for current_item in all_items:
        all_items_names.append(current_item["hash_name"])

all_items_names = list(set(all_items_names))
print(all_items_names)

with open(game_id + "_custom_item_names.docx", "wb") as file:
    pickle.dump(all_items_names, file)
