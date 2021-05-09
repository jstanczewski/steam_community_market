from time import sleep
from decouple import config
import requests
from data_gathering_for_custom_items import item_prices, item_quantity

item_names = [
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
    # "Operation Phoenix Weapon Case",
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

bot_api_key = config("BOT_API_KEY")
chat_id = config("CHAT_ID")
current_run = 1
while True:
    current_run = 1
    for item in item_names:
        run_info = f"{str(current_run)} out of {str(len(item_names))} items"
        text = run_info + "\n" + item_prices(item) + "\n" + item_quantity(item)
        text = text.replace("%", "%25").replace(" ", "%20").replace("&", "%26")
        http = (
            "https://api.telegram.org/bot"
            + bot_api_key
            + "/sendMessage?chat_id="
            + chat_id
            + "&text="
            + text
        )

        requests.get(http)
        current_run += 1
        sleep(2)
    sleep(300)
